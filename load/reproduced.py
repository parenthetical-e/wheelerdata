import numpy as np
from numpy.random import rand

import pandas as pd

from simfMRI.expclass import Reproduce
from simfMRI.noise import white

from fmrilearn.preprocess.labels import csv_to_targets
from fmrilearn.preprocess.labels import targets_to_csv
from fmrilearn.preprocess.labels import tr_pad_targets
from fmrilearn.preprocess.labels import reprocess_targets
from fmrilearn.preprocess.labels import create_y


def _make_accumulator_array(y, index, 
            drift_noise=False, step_noise=False, z_noise=False,
            drift_noise_param=None, step_noise_param=None,
            z_noise_param=None):
    """Make an array of accumulator trials, adding noise if requested."""
    
    y = np.asarray(y, dtype=np.int)
    index = np.asarray(index, dtype=np.int)
    if index.shape != y.shape:
        raise ValueError("index and y do not match")

    if drift_noise_param == None:
        drift_noise_param = {"loc": 0, "scale" : 0.5}

    if step_noise_param == None:
        step_noise_param = {"loc" : 0, "scale" : 0.2, "size" : 1}
    
    if z_noise_param == None:
        z_noise_param = {"low" : 0.01, "high" : 0.5, "size" : 1}

    accumlator = np.zeros_like(y, dtype=np.float)
    for i in np.unique(index):
        mask = i == index
        condi = y[mask]
        t = len(condi)

        # Are y and index aligned?
        if np.sum(condi == condi[0]) != condi.shape[0]:
            raise ValueError("y and index mistach")
        
        if condi[0] > 0:
            drift = 1  ## Does nothing
            if drift_noise:
                drift = np.abs(np.random.normal(**drift_noise_param))
        
            stepn = np.zeros(t) ## Does nothing
            if step_noise:
                stepn = np.random.normal(**step_noise_param)
            
            zn = 0.0
            if z_noise:
                zn = np.random.uniform(**z_noise_param)

            # Create the ramping (i.e. accumlator) signal for
            # this trial
            ramp = (drift * np.linspace(zn, 1, t)) + stepn
            accumlator[mask] = ramp

    return np.asarray(accumlator)


def _make_decision_array(y, index):
    """Make an array decision trials."""

    y = np.asarray(y, dtype=np.int)
    index = np.asarray(index, dtype=np.int)

    if index.shape != y.shape:
        raise ValueError("index and y do not match") 

    decision = np.zeros_like(y, dtype=np.float)
    for i in np.unique(index):
        mask = i == index
        condi = y[mask]
        t = len(condi)

        # Are y and index aligned?
        if np.sum(condi == condi[0]) != condi.shape[0]:
            raise ValueError("y and index mismatch")
        
        if condi[0] > 0:
            trial = np.zeros(t) 
            trial[-2:] = [0.5, 1] 
                ## Add this very short ramp
                ## to the end of the trial
            decision[mask] = trial
    
    return np.asarray(decision)


# Note: the code strategy used here an for simulated.py is VERY different
# don't compare one to other even though they're outputs are similar.
def make_bold(cond, index, wheelerdata, filtfile=None, TR=2, trname="TR",
        noise_f=white, hrf_f=None, hrf_params=None, 
        n_features=10, n_univariate=None, n_accumulator=None, n_decision=None, 
        n_noise=None, drift_noise=False, step_noise=False, z_noise=False,
        drift_noise_param=None, step_noise_param=None, z_noise_param=None):

    # ----
    # Process args for feature composition
    if n_noise == None:
        n_noise = 0
    if n_accumulator == None:
        n_accumulator = 0
    if n_decision == None:
        n_decision = 0
    if n_univariate == None:
        n_univariate = (n_features - n_noise - n_accumulator - n_decision)
    
    if (n_features - n_univariate - n_accumulator - n_noise - n_decision) != 0:
        raise ValueError("The number of features don't add up.")

    # Load the wheelerdata in
    # and start lopping
    metas = wheelerdata.get_RT_metadata_paths()

    Xs, ys, yindices = [], [], []
    for meta in metas:
        # Get all metadata
        # and data, preprocess too,
        data = csv_to_targets(meta)
        data = tr_pad_targets(data, trname, data[trname].shape[0], pad=np.nan)

        if filtfile is not None:
            data = reprocess_targets(filtfile, data, np.nan, ("TR", "trialcount"))
        
        # use the metadata to generate y, and the trial index, yindex
        y = create_y(data[cond])
        yindex = data[index]
    
        # make accumulator and decision traces
        if n_accumulator > 0:
            data["accumulator"] = _make_accumulator_array(
                    y, yindex, drift_noise, step_noise, z_noise,
                    drift_noise_param, step_noise_param, z_noise_param)
        if n_decision > 0:
            data["decision"] = _make_decision_array(y, yindex)

        # Finally we get to work, 
        # first create the boldsim object
        # then use it to populate Xmeta
        boldsim = Reproduce(y, data, noise_f=noise_f, 
                hrf_f=hrf_f, hrf_params=hrf_params, TR=TR, prng=None)
        boldsim.create_dm_from_y(convolve=False)

        n_sample_feature = boldsim.dm.shape[0]
        Xmeta = np.zeros((n_sample_feature, n_features))
        
        # 1. univariate features
        start = 0
        stop = n_univariate
        for j in range(start, stop):
            boldsim.create_bold(np.sum(boldsim.dm[:,1:], axis=1))
            Xmeta[:,j] = boldsim.bold

        # 2. accumulator features
        start = stop
        stop = start + n_accumulator
        for j in range(start, stop):
            boldsim.create_bold(data["accumulator"])
            Xmeta[:,j] = boldsim.bold

        # 3. decision features
        start = stop
        stop = start + n_decision
        for j in range(start, stop):
            boldsim.create_bold(data["decision"])
            Xmeta[:,j] = boldsim.bold

        # 4. noise features:
        start = stop
        stop = start + n_noise
        for j in range(start, stop):
            # Drop baseline from noise
            randbold = rand(boldsim.dm.shape[0])
            randbold[boldsim.y == 0] = 0.0
            boldsim.create_bold(randbold)
            Xmeta[:,j] = boldsim.bold

        Xs.append(Xmeta)
        ys.append(y)
        yindices.append(yindex)

    return Xs, ys, yindices


if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    from wheelerdata.load.clock import Clock
    
    clockdata = Clock()
    scodes = clockdata.scodes

    def save_test_results(test_name, Xs, ys, yindices, scodes):
        for X, y, yindex, scode in zip(Xs, ys, yindices, scodes):
            df = pd.DataFrame(X, columns=["f" + str(i) for i in range(X.shape[1])])
            df["y"] = y
            df["yindex"] = yindex
            df.to_csv("{0}_{1}.csv".format(test_name, str(scode)), sep=",", 
                    float_format='%1.6f', index=False, na_rep="NA")

    # Run and save a bunch of test cases data
    test_name = "univariate1f"
    print(test_name)
    Xs, ys, yindices = make_bold("rt", "trialcount", clockdata, 
        filtfile="/data/data2/meta_accumulate/clock/clock_filter_rt_event.json", 
        TR=2, noise_f=lambda N, prng: (np.zeros(N), prng), hrf_f=None, hrf_params=None, 
        n_features=1, n_univariate=1, n_accumulator=None, n_decision=None, 
        n_noise=None, drift_noise=False, step_noise=False)
    save_test_results(test_name, Xs, ys, yindices, scodes)

    test_name = "accumulator1f"
    print(test_name)
    Xs, ys, yindices = make_bold("rt", "trialcount", clockdata, 
        filtfile="/data/data2/meta_accumulate/clock/clock_filter_rt_event.json", 
        TR=2, noise_f=lambda N, prng: (np.zeros(N), prng), hrf_f=None, hrf_params=None, 
        n_features=1, n_univariate=None, n_accumulator=1, n_decision=None, 
        n_noise=None, drift_noise=False, step_noise=False)
    save_test_results(test_name, Xs, ys, yindices, scodes)
    
    test_name = "drift_noise1f"
    print(test_name)
    Xs, ys, yindices = make_bold("rt", "trialcount", clockdata, 
        filtfile="/data/data2/meta_accumulate/clock/clock_filter_rt_event.json", 
        TR=2, noise_f=lambda N, prng: (np.zeros(N), prng), hrf_f=None, hrf_params=None, 
        n_features=1, n_univariate=None, n_accumulator=1, n_decision=None, 
        n_noise=None, drift_noise=True, step_noise=False)
    save_test_results(test_name, Xs, ys, yindices, scodes)
    
    test_name = "step_noise1f"
    print(test_name)
    Xs, ys, yindices = make_bold("rt", "trialcount", clockdata, 
        filtfile="/data/data2/meta_accumulate/clock/clock_filter_rt_event.json", 
        TR=2, noise_f=lambda N, prng: (np.zeros(N), prng), hrf_f=None, hrf_params=None, 
        n_features=1, n_univariate=None, n_accumulator=1, n_decision=None, 
        n_noise=None, drift_noise=False, step_noise=True)
    save_test_results(test_name, Xs, ys, yindices, scodes)

    test_name = "z_noise1f"
    print(test_name)
    Xs, ys, yindices = make_bold("rt", "trialcount", clockdata, 
        filtfile="/data/data2/meta_accumulate/clock/clock_filter_rt_event.json", 
        TR=2, noise_f=lambda N, prng: (np.zeros(N), prng), hrf_f=None, hrf_params=None, 
        n_features=1, n_univariate=None, n_accumulator=1, n_decision=None, 
        n_noise=None, drift_noise=False, step_noise=False, z_noise=True)
    save_test_results(test_name, Xs, ys, yindices, scodes)

    test_name = "decision1f"
    print(test_name)
    Xs, ys, yindices = make_bold("rt", "trialcount", clockdata, 
        filtfile="/data/data2/meta_accumulate/clock/clock_filter_rt_event.json", 
        TR=2, noise_f=lambda N, prng: (np.zeros(N), prng), hrf_f=None, hrf_params=None, 
        n_features=1, n_univariate=None, n_accumulator=None, n_decision=1, 
        n_noise=None, drift_noise=False, step_noise=False)
    save_test_results(test_name, Xs, ys, yindices, scodes)

    test_name = "noise1f"
    print(test_name)
    Xs, ys, yindices = make_bold("rt", "trialcount", clockdata, 
        filtfile="/data/data2/meta_accumulate/clock/clock_filter_rt_event.json", 
        TR=2, noise_f=lambda N, prng: (np.zeros(N), prng), hrf_f=None, hrf_params=None, 
        n_features=1, n_univariate=None, n_accumulator=None, n_decision=None, 
        n_noise=1, drift_noise=False, step_noise=False)
    save_test_results(test_name, Xs, ys, yindices, scodes)

    test_name = "uni_acc_dec_noi4f"
    print(test_name)
    Xs, ys, yindices = make_bold("rt", "trialcount", clockdata, 
        filtfile="/data/data2/meta_accumulate/clock/clock_filter_rt_event.json", 
        TR=2, noise_f=lambda N, prng: (np.zeros(N), prng), hrf_f=None, hrf_params=None, 
        n_features=4, n_univariate=1, n_accumulator=1, n_decision=1, 
        n_noise=1, drift_noise=False, step_noise=False)
    save_test_results(test_name, Xs, ys, yindices, scodes)

    test_name = "withnoise4f"
    print(test_name)
    Xs, ys, yindices = make_bold("rt", "trialcount", clockdata, 
        filtfile="/data/data2/meta_accumulate/clock/clock_filter_rt_event.json", 
        TR=2, noise_f=white, hrf_f=None, hrf_params=None, 
        n_features=4, n_univariate=1, n_accumulator=1, n_decision=1, 
        n_noise=1, drift_noise=False, step_noise=False)
    save_test_results(test_name, Xs, ys, yindices, scodes)

