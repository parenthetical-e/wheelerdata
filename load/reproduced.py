import numpy as np
from numpy.random import RandomState
from numpy.random import rand

import pandas as pd

from simfMRI.expclass import Reproduce
from simfMRI.noise import white

from fmrilearn.preprocess.labels import csv_to_targets
from fmrilearn.preprocess.labels import targets_to_csv
from fmrilearn.preprocess.labels import tr_pad_targets
from fmrilearn.preprocess.labels import reprocess_targets
from fmrilearn.preprocess.labels import create_y
from fmrilearn.preprocess.labels import unique_nan


def _shorten_mask(mask, t):
    # Shorten mask to t
    mask_cnt = 1
    for mask_i, ma in enumerate(mask):
        if ma:
            if mask_cnt > t:
                mask[mask_i] = False
            mask_cnt += 1
    assert np.sum(mask) == t, "mask rt mismatch"

    return mask


def _make_accumulator_array(y, index, cond_to_rt,
            drift_noise=False, step_noise=False, z_noise=False,
            drift_noise_param=None, step_noise_param=None,
            z_noise_param=None, prng=None, baseline=(0, np.nan, 'nan')):
    """Make an array of accumulator trials, adding noise if requested."""
    
    if prng == None:
        prng = RandomState()

    y = np.asarray(y, dtype=np.int)
    index = np.asarray(index, dtype=np.int)
    if index.shape != y.shape:
        raise ValueError("index and y do not match")

    if drift_noise_param == None:
        drift_noise_param = {"loc": 0, "scale" : 0.5}

    if step_noise_param == None:
        step_noise_param = {"loc" : 0, "scale" : 0.2, "size" : 1}
    
    if z_noise_param == None:
        z_noise_param = {"low" : 0.1, "high" : 0.5, "size" : 1}

    accumlator = np.zeros_like(y, dtype=np.float)
    for i in np.unique(index):
        mask = index == i
        condi = y[mask]
        t = cond_to_rt[condi[0]]
        
        # Skip baseline
        if i in baseline:
            continue
        if condi[0] in baseline:
            continue
            
        # Sanity
        if t <= 0:
            raise ValueError("{0} had RT of {1}. Too short.".format(condi, t))
        if t > len(condi):
            raise ValueError("{0} had RT of {1}. Too long.".format(condi, t))        
        if np.sum(condi == condi[0]) != condi.shape[0]:
            raise ValueError("y and index mismatch")
            
        mask = _shorten_mask(mask, t)
        
        drift = 1  ## Does nothing
        if drift_noise:
            drift = np.abs(prng.normal(**drift_noise_param))
                ## Now does something
                
        stepn = np.zeros(t)
        if step_noise:
            stepn = prng.normal(**step_noise_param)
        
        zn = 0.1
        if z_noise:
            zn = prng.uniform(**z_noise_param)

        # Create the ramping (i.e. accumlator)
        ramp = (drift * np.linspace(zn, 1, t)) + stepn
        assert len(ramp) == np.sum(mask), "ramp mask mismatch"
        
        accumlator[mask] = ramp

    return np.asarray(accumlator)


def _make_decision_array(y, index, cond_to_rt, baseline=(0, np.nan, 'nan')):
    """Make an array decision trials."""
            
    y = np.asarray(y, dtype=np.int)
    index = np.asarray(index, dtype=np.int)

    if index.shape != y.shape:
        raise ValueError("index and y do not match") 

    decision = np.zeros_like(y, dtype=np.float)
    for i in np.unique(index):
        mask = index == i
        condi = y[mask]
        t = cond_to_rt[condi[0]]
        
        # Skip baseline
        if i in baseline:
            continue
        if condi[0] in baseline:
            continue
        
        # Sanity
        if t <= 0:
            raise ValueError("{0} had RT of {1}. Too short.".format(condi, t))
        if t > len(condi):
            raise ValueError("{0} had RT of {1}. Too long.".format(condi, t))
            
        # Are y and index aligned?
        if np.sum(condi == condi[0]) != condi.shape[0]:
            raise ValueError("y and index mismatch")
        
        mask = _shorten_mask(mask, t)
        
        trial = np.zeros(t)
        if len(trial) == 1:
            trial[-1:] = [1]
        else:
            trial[-2:] = [0.5, 1] 
                ## Add this very short ramp
                ## to the end of the trial
        decision[mask] = trial
    
    return np.asarray(decision)


def make_bold(cond, index, wheelerdata, cond_to_rt, filtfile=None, TR=2, trname="TR",
        n_features=10, n_univariate=None, n_accumulator=None, n_decision=None, 
        n_noise=None, drift_noise=False, step_noise=False, z_noise=False,
        drift_noise_param=None, step_noise_param=None, z_noise_param=None,
        noise_f=white, hrf_f=None, hrf_params=None, prng=None):
    """Make BOLD timecourse features based on Wheelerdata

    Parameters
    ---------
    cond : str
        A condition name found in the wheelerdata objects metadata
    index : str
        A name of a trial index found in the wheelerdata object metadata
    wheelerdata : object, instance of Wheelerdata
        A Wheelerdata object
    cond_to_rt: dict
        A map of cond (key) to reaction time (item, (int, float))
    filtfile : str, None
        A name of json file designed for reprocessing Wheelerdata metadata
    TR : float, int
        The repitition time of the experiement
    trname : str
        The name of the index of TRs in the metadata
    n_features : int
        The number of features in total (other n_* arguements
        must sum to this value
    n_univariate : int
        The number of univariate (boxcar) features
    n_accumulator : int
        The number of accumulator features
    n_decision : int
        The number of decision features
    n_noise : int
        The number of noise features
    drift_noise : boolean, optional
        Add noise to the drift rate of the accumulator features
    step_noise : boolean, optional
        Add Noise to each step accumulator features
    z_noise : boolean, optional
        Add noise to the start value of accumulator features
    drift_noise_param : None or dict, optional
        Parameters for drift_noise which is drawn from a
        Gaussian distribution. None defaults to: 
        `{"loc": 0, "scale" : 0.5}`
    step_noise_param : None or dict, optional
        Parameters for step_noise which is drawn from a 
        Gaussian distribution. None defaults to:
        `{"loc" : 0, "scale" : 0.2, "size" : 1}`
    z_noise_param : None or dict, optional
        Parameters for z_noise which is drawn from the uniform
        distribution. None defaults to:
        `{"low" : 0.01, "high" : 0.5, "size" : 1}`
    noise_f : function, optional
        Produces noise, must have signatures like `noise, prng = f(N, prng)`
    hrf_f : function, optional
        Returns a haemodynamic response, signature hrf_f(**hrf_params)
    hrf_params : dict
        Keyword parameters for hrf_f
    prng : None or RandomState object
        Allows for independent random draws, used for all 
        random sampling
    """

    # ----
    # Feature composition
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

    # Load wheelerdata
    metas = wheelerdata.get_RT_metadata_paths()

    # Get to work simulating
    Xs, ys, yindices = [], [], []
    for meta in metas:
        # Get data, preprocess too,
        data = csv_to_targets(meta)
        data = tr_pad_targets(data, trname, data[trname].shape[0], pad=np.nan)

        if filtfile is not None:
            data = reprocess_targets(
                    filtfile, data, np.nan, ("TR", "trialcount")
                    )
        
        # Check cond_to_rt
        for c in unique_nan(data[cond]):
            try:
                cond_to_rt[c]
            except KeyError:
                raise KeyError("{0} not present in cond_to_rt".format(c))
        
        # use cond to create y
        y = create_y(data[cond])
        yindex = data[index]
    
        # make accumulator and decision traces
        if n_accumulator > 0:
            data["accumulator"] = _make_accumulator_array(
                    y, yindex, cond_to_rt, drift_noise, step_noise, z_noise,
                    drift_noise_param, step_noise_param, z_noise_param,
                    prng=prng)
        if n_decision > 0:
            data["decision"] = _make_decision_array(y, yindex, cond_to_rt)

        # Populate Xmeta
        boldsim = Reproduce(y, data, noise_f=noise_f, 
                hrf_f=hrf_f, hrf_params=hrf_params, TR=TR, prng=prng)
        boldsim.create_dm_from_y(convolve=False)

        n_sample_feature = boldsim.dm.shape[0]
        Xmeta = np.zeros((n_sample_feature, n_features))
        
        # 1. univariate features
        start = 0
        stop = n_univariate
        for j in range(start, stop):
            boldsim.create_bold(np.sum(boldsim.dm[:,1:], axis=1), convolve=True)
            Xmeta[:,j] = boldsim.bold

        # 2. accumulator features
        start = stop
        stop = start + n_accumulator
        for j in range(start, stop):
            boldsim.create_bold(data["accumulator"], convolve=True)
            Xmeta[:,j] = boldsim.bold

        # 3. decision features
        start = stop
        stop = start + n_decision
        for j in range(start, stop):
            boldsim.create_bold(data["decision"], convolve=True)
            Xmeta[:,j] = boldsim.bold

        # 4. noise features:
        start = stop
        stop = start + n_noise
        for j in range(start, stop):
            # Drop baseline from noise
            randbold = rand(boldsim.dm.shape[0])
            randbold[boldsim.y == 0] = 0.0
            boldsim.create_bold(randbold, convolve=True)
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
    prng = RandomState(42)

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
        n_noise=None, drift_noise=False, step_noise=False, prng=prng)
    save_test_results(test_name, Xs, ys, yindices, scodes)

    test_name = "accumulator1f"
    print(test_name)
    Xs, ys, yindices = make_bold("rt", "trialcount", clockdata, 
        filtfile="/data/data2/meta_accumulate/clock/clock_filter_rt_event.json", 
        TR=2, noise_f=lambda N, prng: (np.zeros(N), prng), hrf_f=None, hrf_params=None, 
        n_features=1, n_univariate=None, n_accumulator=1, n_decision=None, 
        n_noise=None, drift_noise=False, step_noise=False, prng=prng)
    save_test_results(test_name, Xs, ys, yindices, scodes)
    
    test_name = "drift_noise1f"
    print(test_name)
    Xs, ys, yindices = make_bold("rt", "trialcount", clockdata, 
        filtfile="/data/data2/meta_accumulate/clock/clock_filter_rt_event.json", 
        TR=2, noise_f=lambda N, prng: (np.zeros(N), prng), hrf_f=None, hrf_params=None, 
        n_features=1, n_univariate=None, n_accumulator=1, n_decision=None, 
        n_noise=None, drift_noise=True, step_noise=False, prng=prng)
    save_test_results(test_name, Xs, ys, yindices, scodes)
    
    test_name = "step_noise1f"
    print(test_name)
    Xs, ys, yindices = make_bold("rt", "trialcount", clockdata, 
        filtfile="/data/data2/meta_accumulate/clock/clock_filter_rt_event.json", 
        TR=2, noise_f=lambda N, prng: (np.zeros(N), prng), hrf_f=None, hrf_params=None, 
        n_features=1, n_univariate=None, n_accumulator=1, n_decision=None, 
        n_noise=None, drift_noise=False, step_noise=True, prng=prng)
    save_test_results(test_name, Xs, ys, yindices, scodes)

    test_name = "z_noise1f"
    print(test_name)
    Xs, ys, yindices = make_bold("rt", "trialcount", clockdata, 
        filtfile="/data/data2/meta_accumulate/clock/clock_filter_rt_event.json", 
        TR=2, noise_f=lambda N, prng: (np.zeros(N), prng), hrf_f=None, hrf_params=None, 
        n_features=1, n_univariate=None, n_accumulator=1, n_decision=None, 
        n_noise=None, drift_noise=False, step_noise=False, z_noise=True, prng=prng)
    save_test_results(test_name, Xs, ys, yindices, scodes)

    test_name = "decision1f"
    print(test_name)
    Xs, ys, yindices = make_bold("rt", "trialcount", clockdata, 
        filtfile="/data/data2/meta_accumulate/clock/clock_filter_rt_event.json", 
        TR=2, noise_f=lambda N, prng: (np.zeros(N), prng), hrf_f=None, hrf_params=None, 
        n_features=1, n_univariate=None, n_accumulator=None, n_decision=1, 
        n_noise=None, drift_noise=False, step_noise=False, prng=prng)
    save_test_results(test_name, Xs, ys, yindices, scodes)

    test_name = "noise1f"
    print(test_name)
    Xs, ys, yindices = make_bold("rt", "trialcount", clockdata, 
        filtfile="/data/data2/meta_accumulate/clock/clock_filter_rt_event.json", 
        TR=2, noise_f=lambda N, prng: (np.zeros(N), prng), hrf_f=None, hrf_params=None, 
        n_features=1, n_univariate=None, n_accumulator=None, n_decision=None, 
        n_noise=1, drift_noise=False, step_noise=False, prng=prng)
    save_test_results(test_name, Xs, ys, yindices, scodes)

    test_name = "uni_acc_dec_noi4f"
    print(test_name)
    Xs, ys, yindices = make_bold("rt", "trialcount", clockdata, 
        filtfile="/data/data2/meta_accumulate/clock/clock_filter_rt_event.json", 
        TR=2, noise_f=lambda N, prng: (np.zeros(N), prng), hrf_f=None, hrf_params=None, 
        n_features=4, n_univariate=1, n_accumulator=1, n_decision=1, 
        n_noise=1, drift_noise=False, step_noise=False, prng=prng)
    save_test_results(test_name, Xs, ys, yindices, scodes)

    test_name = "withnoise4f"
    print(test_name)
    Xs, ys, yindices = make_bold("rt", "trialcount", clockdata, 
        filtfile="/data/data2/meta_accumulate/clock/clock_filter_rt_event.json", 
        TR=2, noise_f=white, hrf_f=None, hrf_params=None, 
        n_features=4, n_univariate=1, n_accumulator=1, n_decision=1, 
        n_noise=1, drift_noise=False, step_noise=False, prng=prng)
    save_test_results(test_name, Xs, ys, yindices, scodes)

