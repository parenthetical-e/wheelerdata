import numpy as np
from numpy.random import RandomState
from wheelerdata.load.reproduced import _make_accumulator_array
from wheelerdata.load.reproduced import _make_decision_array
from wheelerdata.load.reproduced import _shorten_mask
    

def test___shorten_mask():
    ntrue = 10
    
    # t < mask
    testn = 1
    t = 5
    mask = np.ones(ntrue) == 1
    assert np.sum(mask) == ntrue
    assert np.sum(_shorten_mask(mask, t)) == t, (
            "t short mismatch at test {0}".format(testn)
    )
    # t == mask
    testn = 2
    t = 10
    mask = np.ones(ntrue) == 1
    assert np.sum(mask) == ntrue
    assert np.sum(_shorten_mask(mask, t)) == t, (
            "t short mismatch at test {0}".format(testn)
    )
    # t is null
    testn = 3
    t = 0
    mask = np.ones(ntrue) == 1
    assert np.sum(mask) == ntrue
    assert np.sum(_shorten_mask(mask, t)) == t, (
            "t short mismatch at test {0}".format(testn)
    )
    # t is in the middle
    testn = 1
    t = 5
    mask = np.concatenate([np.zeros(5), np.ones(ntrue), np.zeros(5)]) == 1
    assert np.sum(mask) == ntrue
    assert np.sum(_shorten_mask(mask, t)) == t, (
            "t short mismatch at test {0}".format(testn)
    )
    
    
def test___make_accumulator_array():
    # _make_accumulator_array(y, index, cond_to_rt,
    #             drift_noise=False, step_noise=False, z_noise=False,
    #             drift_noise_param=None, step_noise_param=None,
    #             z_noise_param=None, prng=None):

    prng = np.random.RandomState(42)

    # Create data
    # 2 conds
    n = 20   ## number of events
    l = 5
    rt1 = 2
    rt2 = 4
    cond_to_rt = {0:0, 1:rt1, 2:rt2}
    
    iti = (1,6) ## Jitter range (Uniform dist)
    tr = 2      ## TR in s
    l_in_tr = l/tr ## TR in TR 

    y = []
    index = []
    for i in range(1, n+1):
        cond = [prng.randint(1,3)] * l
        jitter = [0] * prng.randint(iti[0],iti[1]+1) 
        y.extend(cond + jitter)
        index.extend([i]*len(cond) + jitter)
     
    # Go!       
    accum = _make_accumulator_array(y, index, cond_to_rt)
    
    # Compare accum ramps to correct ramps
    correct_ramps = {
        rt1: [0.1, 1],
        rt2: [0.1, 0.4, 0.7, 1.]
    }
    
    for index_i in np.unique(index):
        mask = index == index_i
        cond = np.asarray(y)[mask][0]
        rt = cond_to_rt[cond]
        mask = _shorten_mask(mask, rt)
        
        if rt > 0:
            correct = correct_ramps[rt]
            assert np.allclose(correct, accum[mask]), "incorrect ramp"

    
def test__make_decision_array():
    # def _make_decision_array(y, index, cond_to_rt, baseline=0):
    
    prng = np.random.RandomState(42)

    # Create data
    # 2 conds
    n = 20   ## number of events
    l = 5
    rt1 = 1
    rt2 = 3
    cond_to_rt = {0:0, 1:rt1, 2:rt2}
    
    iti = (1,6) ## Jitter range (Uniform dist)
    tr = 2      ## TR in s
    l_in_tr = l/tr ## TR in TR 

    y = []
    index = []
    for i in range(1, n+1):
        cond = [prng.randint(1,3)] * l
        jitter = [0] * prng.randint(iti[0],iti[1]+1) 
        y.extend(cond + jitter)
        index.extend([i]*len(cond) + jitter)
     
    # Go!       
    accum = _make_decision_array(y, index, cond_to_rt)
    
    # Compare accum ramps to correct ramps
    correct_ramps = {
        rt1: [1.],
        rt2: [0.0, 0.5, 1.]
    }
    
    for index_i in np.unique(index):
        mask = index == index_i
        cond = np.asarray(y)[mask][0]
        rt = cond_to_rt[cond]
        mask = _shorten_mask(mask, rt)
        
        if rt > 0:
            correct = correct_ramps[rt]
            assert np.allclose(correct, accum[mask]), "incorrect ramp"
    