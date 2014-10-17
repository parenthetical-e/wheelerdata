"""Make or load test datasets."""
import numpy as np

from functools import partial
from numpy.random import random_integers
from sklearn.preprocessing import scale

import simfMRI.noise as noisefns
from simfMRI.expclass import Exp
from simBehave.trials import event_random
from simfMRI.misc import process_prng


class _NCond(Exp):

    """
    Simulate N conditions using one then the other as the BOLD signal.

    Parameters
    ----------
    n - total trial count
    n_cond - the number of conditions
    TR - The sampling time
    durations - a range of durations [start, stop] (e.g. [2,6] give a
        duration range from [2,6] randomly sampled from a uniform
        distribution) Default = None ( = 1).
    noise - The noise models to use (default = white, options are
        ar1, physio, white, lowfreqdrift)
    """

    def __init__(self, n, n_cond=2, TR=2, durations=None,):
        try:
            Exp.__init__(self, TR=TR, ISI=2, prng=None)
        except AttributeError:
            pass

        self.trials, self.prng = event_random(n_cond, n, 1, self.prng)
        self.trials = np.array(self.trials)
        if durations != None:
            start, stop = durations[0], durations[1]
            self.durations = [random_integers(start, stop) for
                              _ in self.trials]
        else:
            self.durations = [1, ] * len(self.trials)


class _Ar1(_NCond):

    """_NCond with an AR(1) noise model.

    Parameters
    ----------
    alpha - the degree of AR(1) autocorrelation (0-1).
    """

    def __init__(self, n, n_cond=2, TR=2, durations=None, alpha=0.5):
          # Init _NCond.
        _NCond.__init__(self, n=n, n_cond=n_cond, TR=TR, durations=durations)

        # Then override the noise_f
        self.noise_f = partial(getattr(noisefns, "ar1"), alpha=alpha)


class _Physio(_NCond):

    """_NCond with an 'physiological' noise model.

    Parameters
    ----------
    See 'physio' in simfMRI.noise for the parametrization.
    """

    def __init__(self, n, n_cond=2, TR=2, durations=None, sigma=1,
                 freq_heart=1.17, freq_resp=0.2):
        # Init _NCond.
        _NCond.__init__(self, n=n, n_cond=n_cond, TR=TR, durations=durations)

        # Then override the noise_f
        self.noise_f = partial(getattr(noisefns, "physio"),
                               TR=TR, sigma=sigma, freq_heart=freq_heart, freq_resp=freq_resp)


def _selectExp(noise):
    """Select a BOLD sim experimental class based on the noise type."""

    # ----
    # Detect noise, then use PFA to enforce a constant
    # signature on ExpClass; what a mess, so so sorry.
    if noise == "white":
        ExpClass = _NCond
    elif noise == "ar1":
        ExpClass = partial(_Ar1, alpha=0.5)
    elif noise == "physio":
        ExpClass = partial(_Physio, sigma=1, freq_heart=1.17, freq_resp=0.2)
    else:
        raise ValueError("noise was not understood.")

    return ExpClass


def _univariate_features(n, boldsim):
    """Create n univariate features."""

    Xuni = np.zeros((boldsim.dm.shape[0], n))
    arr = scale(boldsim.dm[:, 0:].sum(1), with_mean=False)  # Rescale
    for jj in range(n):
        # Generate a (new) BOLD model (i.e. new noise)
        boldsim.create_bold(arr, convolve=False)
        # To make the bold, combine dm cols: sum all but the
        # first col, which is the baseline.

        Xuni[:, jj] = boldsim.bold

    return Xuni


def _noise_features(n, boldsim):
    """Create n noise-only features."""

    Xnoise = np.zeros((boldsim.dm.shape[0], n))
    for jj in range(n):
        boldsim.create_bold(np.zeros(boldsim.dm.shape[0]), convolve=False)
        # By passing an array of 0's, we get only noise out.
        Xnoise[:, jj] = boldsim.bold

    return Xnoise


def _accumulator_features(n, boldsim, drift_noise=False, step_noise=False):
    """Create n accumulator-like features. Also return the accumulators
    array. """

    accumulators = _make_accumulator_array(boldsim.trials, boldsim.durations,
                                           drift_noise=drift_noise, step_noise=step_noise)
    Xacc = np.zeros((accumulators.shape[0], n))
    for jj in range(n):
        boldsim.create_bold(accumulators, convolve=True)
        Xacc[:, jj] = boldsim.bold

    return Xacc, accumulators


def _decision_features(n, boldsim):
    """Create n decision-like (impulse at TR) features. Also return the
    decision array."""

    decisions = _make_decision_array(boldsim.trials, boldsim.durations)
    Xdec = np.zeros((decisions.shape[0], n))
    for jj in range(n):
        boldsim.create_bold(decisions, convolve=True)
        Xdec[:, jj] = boldsim.bold

    return Xdec, decisions


def _repeated_features(n, n_informative, X):
    """Randomly select and copy n features from X, from the col 
    range [0 ... n_informative].
    """
    Xrep = np.zeros((X.shape[0], n))
    for jj in range(n):
        rand_info_col = np.random.random_integers(0, n_informative - 1)
        Xrep[:, jj] = X[:, rand_info_col]

    return Xrep


def _make_decision_array(trials, durations):
    """Treat trials as reaction times, and use these rts to create 
    mock decision signals.
    """

    decision = []
    for t, d in zip(trials, durations):
        if t == 0:
            decision.extend([0, ] * d)  # Add empty trial if t == 0
        else:
            trial = np.zeros(d)  # Init this trial's data
            trial[t - 1] = 1.0
            decision.extend(trial.tolist())

    return np.array(decision)


def _make_accumulator_array(trials, durations, drift_noise=False,
                            step_noise=False):
    """Treat trials as reaction times, and use these rts to create
    mock accumulator signals whose drift rates and step sizes 
    could be Gaussian processes.

    Note:
    -----
    Noise processes for both drift and step normal Gaussians with 
    the following params:

    drift : M = 0, SD = 0.5
    step : M = 0, SD = .2  

    The SD in both cases is arbitrary. I played with the SDs until the
    noised curves looked plausible - not to much noise, not to little.
    As I'm primarily worried about the impact these noise processes 
    have on BOLD frequency not magnitude this seems a justifiable, at
    least in the short term.
    """

    accumlator = []
    for t, d in zip(trials, durations):
        if t == 0:
            accumlator.extend([0, ] * d)
            # Add empty trial if t == 0
        else:
            trial = np.zeros(d)
            # Init this trial's data

            # Drift rate is noisy?
            drift = 1  # Does nothing
            if drift_noise:
                drift = np.abs(np.random.normal(loc=0, scale=0.5))

                # Drift params: Mean 0, SD = 0.1

            # Steps are noisy?
            stepn = np.zeros(t)  # Does nothing
            if step_noise:
                stepn = np.random.normal(loc=0, scale=0.2, size=t)

            # Create the ramping (i.e. accumlator) signal for
            # this trial
            ramp = drift * (np.arange(1, t + 1) / np.float(t))

            # Update trial with ramp and add to the accumlator trace
            trial[:len(ramp)] = ramp + stepn
            accumlator.extend(trial.tolist())

    return np.array(accumlator)


def _generate_labels(boldsim):
    """Use the boldsim data to create and return reaction time 
    and trial-level labels.
    """

    # Now use trials and durations to generate labals (i.e., y).
    y = []
    y_trialcount = []
    indext = range(len(boldsim.trials))
    for t, d, i in zip(boldsim.trials, boldsim.durations, indext):
        t_in_d = [t, ] * d
        y.extend(t_in_d)

        t_count = [i, ] * d
        y_trialcount.extend(t_count)

    y = np.array(y)  # In metacculate the standard is for
    # labels to be in in arrays not lists
    y_trialcount = np.array(y_trialcount)

    return y, y_trialcount


def make_bold(n_cond, n_trials_per_cond, TR=2, durations=[8, 16],
              noise="white", n_features=10, n_univariate=None,
              n_accumulator=None, n_decision=None, n_noise=None, n_repeated=None,
              drift_noise=False, step_noise=False):
    """Make a simple BOLD dataset.

    Note:
    ----
    Defaults to creating univariate features.
    """

    # ----
    # Process args for feature composition
    if n_noise == None:
        n_noise = 0
    if n_repeated == None:
        n_repeated = 0
    if n_accumulator == None:
        n_accumulator = 0
    if n_decision == None:
        n_decision = 0
    if n_univariate == None:
        n_univariate = (n_features - n_noise - n_repeated - n_accumulator
                        - n_decision)

    if (n_features - n_univariate - n_accumulator - n_noise
            - n_repeated - n_decision) != 0:
        raise ValueError("The number of features don't add up.")

    # ----
    # Select the BOLD sim class based on noise type
    ExpClass = _selectExp(noise)

    # ----
    # Get to work....
    #
    # Instantiate a BOLD generator.
    boldsim = ExpClass(n_trials_per_cond, n_cond, TR=2, durations=durations)
    numactive = 8
    drop = [0, ] * numactive + [1, ] * (max(durations) - numactive)
    # Simulate a trial structure where the neural
    # impulse spans from TR 0 to numactive. See
    # dtime() in simfMRI.timing for an explanation
    # of drop's structure.

    boldsim.create_dm(convolve=True, drop=drop)

    # Init X, the features
    n_sample_feature = boldsim.dm.shape[0]
    X = np.zeros((n_sample_feature, n_features))

    # And build up X
    # 1. univariate features
    start = 0
    stop = n_univariate
    X[:, start:stop] = _univariate_features(n_univariate, boldsim)

    # 2. accumulator features
    start = stop
    stop = start + n_accumulator
    X[:, start:stop], acc = _accumulator_features(n_accumulator, boldsim,
                                                  drift_noise=drift_noise, step_noise=step_noise)

    # 3. decision features
    start = stop
    stop = start + n_decision
    X[:, start:stop], dec = _decision_features(n_decision, boldsim)

    # 4. noise features:
    start = stop
    stop = start + n_noise
    X[:, start:stop] = _noise_features(n_noise, boldsim)

    # 5. feature repeats
    start = stop
    stop = start + n_repeated
    X[:, start:stop] = _repeated_features(n_repeated,
                                          (n_univariate + n_accumulator), X)

    # 6. Create labels
    y, y_trialcount = _generate_labels(boldsim)

    return X, y, y_trialcount


if __name__ == "__main__":
    """For later testing and analysis, save a variety of simulated BOLD
    timecourses as csv files."""

    # ----
    # GLOBALS
    n_c = 7
    n_t_c = 10
    ds = [8, 16]
    n_f = 3
    n_iter = 3

    # ----
    # univariate
    noise = "physio"
    for ii in range(n_iter):
        X, y, tcs = make_bold(
            n_c, n_t_c,
            TR=2,
            durations=ds,
            noise="physio",
            n_features=n_f,
            n_univariate=None,
            n_accumulator=None,
            n_decision=None,
            n_noise=None,
            n_repeated=None,
            drift_noise=False,
            step_noise=False)
        np.savetxt('uni_' + noise + '_' + str(ii) + '.csv', X,
                   fmt='%1.6f', delimiter=",")

    noise = "ar1"
    for ii in range(n_iter):
        X, y, tcs = make_bold(
            n_c, n_t_c,
            TR=2,
            durations=ds,
            noise="ar1",
            n_features=n_f,
            n_univariate=None,
            n_accumulator=None,
            n_decision=None,
            n_noise=None,
            n_repeated=None,
            drift_noise=False,
            step_noise=False)
        np.savetxt('uni_' + noise + '_' + str(ii) + '.csv', X,
                   fmt='%1.6f', delimiter=",")

    # ----
    # accumulator
    noise = "physio"
    for ii in range(n_iter):
        X, y, tcs = make_bold(
            n_c, n_t_c,
            TR=2,
            durations=ds,
            noise="physio",
            n_features=n_f,
            n_univariate=None,
            n_accumulator=n_f,
            n_decision=None,
            n_noise=None,
            n_repeated=None,
            drift_noise=False,
            step_noise=False)
        np.savetxt('acc_' + noise + '_' + str(ii) + '.csv', X,
                   fmt='%1.6f', delimiter=",")

    noise = "ar1"
    for ii in range(n_iter):
        X, y, tcs = make_bold(
            n_c, n_t_c,
            TR=2,
            durations=ds,
            noise="ar1",
            n_features=n_f,
            n_univariate=None,
            n_accumulator=n_f,
            n_decision=None,
            n_noise=None,
            n_repeated=None,
            drift_noise=False,
            step_noise=False)
        np.savetxt('acc_' + noise + '_' + str(ii) + '.csv', X,
                   fmt='%1.6f', delimiter=",")

    # ----
    # accumulator + drift noise
    noise = "physio"
    for ii in range(n_iter):
        X, y, tcs = make_bold(
            n_c, n_t_c,
            TR=2,
            durations=ds,
            noise="physio",
            n_features=n_f,
            n_univariate=None,
            n_accumulator=n_f,
            n_decision=None,
            n_noise=None,
            n_repeated=None,
            drift_noise=True,
            step_noise=False)
        np.savetxt('drift_' + noise + '_' + str(ii) + '.csv', X,
                   fmt='%1.6f', delimiter=",")

    noise = "ar1"
    for ii in range(n_iter):
        X, y, tcs = make_bold(
            n_c, n_t_c,
            TR=2,
            durations=ds,
            noise="ar1",
            n_features=n_f,
            n_univariate=None,
            n_accumulator=n_f,
            n_decision=None,
            n_noise=None,
            n_repeated=None,
            drift_noise=True,
            step_noise=False)
        np.savetxt('drift_' + noise + '_' + str(ii) + '.csv', X,
                   fmt='%1.6f', delimiter=",")

    # ----
    # accumulator + step
    noise = "physio"
    for ii in range(n_iter):
        X, y, tcs = make_bold(
            n_c, n_t_c,
            TR=2,
            durations=ds,
            noise="physio",
            n_features=n_f,
            n_univariate=None,
            n_accumulator=n_f,
            n_decision=None,
            n_noise=None,
            n_repeated=None,
            drift_noise=False,
            step_noise=True)
        np.savetxt('step_' + noise + '_' + str(ii) + '.csv', X,
                   fmt='%1.6f', delimiter=",")

    noise = "ar1"
    for ii in range(n_iter):
        X, y, tcs = make_bold(
            n_c, n_t_c,
            TR=2,
            durations=ds,
            noise="ar1",
            n_features=n_f,
            n_univariate=None,
            n_accumulator=n_f,
            n_decision=None,
            n_noise=None,
            n_repeated=None,
            drift_noise=False,
            step_noise=True)
        np.savetxt('step_' + noise + '_' + str(ii) + '.csv', X,
                   fmt='%1.6f', delimiter=",")

    # ----
    # decision
    noise = "physio"
    for ii in range(n_iter):
        X, y, tcs = make_bold(
            n_c, n_t_c,
            TR=2,
            durations=ds,
            noise="physio",
            n_features=n_f,
            n_univariate=None,
            n_accumulator=None,
            n_decision=n_f,
            n_noise=None,
            n_repeated=None,
            drift_noise=False,
            step_noise=False)
        np.savetxt('dec_' + noise + '_' + str(ii) + '.csv', X,
                   fmt='%1.6f', delimiter=",")

    noise = "ar1"
    for ii in range(n_iter):
        X, y, tcs = make_bold(
            n_c, n_t_c,
            TR=2,
            durations=ds,
            noise="ar1",
            n_features=n_f,
            n_univariate=None,
            n_accumulator=None,
            n_decision=n_f,
            n_noise=None,
            n_repeated=None,
            drift_noise=False,
            step_noise=False)
        np.savetxt('dec_' + noise + '_' + str(ii) + '.csv', X,
                   fmt='%1.6f', delimiter=",")
