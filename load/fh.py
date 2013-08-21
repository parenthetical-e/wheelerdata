from fmrilearn.load import load_nifti

# ----
# Global pathing...
ROIPATH = "/data/data2/meta_accumulate/fh/roinii"    
METAPATH = "/data/data2/meta_accumulate/fh/fidl"

def get_roi_data_paths(roi):
    return [
        os.path.join(ROIPATH, roi+"_9.nii.gz"),
        os.path.join(ROIPATH, roi+"_11.nii.gz"),
        os.path.join(ROIPATH, roi+"_13.nii.gz"),
        os.path.join(ROIPATH, roi+"_14.nii.gz"),
        os.path.join(ROIPATH, roi+"_15.nii.gz"),
        os.path.join(ROIPATH, roi+"_17.nii.gz"),
        os.path.join(ROIPATH, roi+"_19.nii.gz"),
        os.path.join(ROIPATH, roi+"_21.nii.gz"),
        os.path.join(ROIPATH, roi+"_23.nii.gz"),
        os.path.join(ROIPATH, roi+"_24.nii.gz"),
        os.path.join(ROIPATH, roi+"_25.nii.gz"),
        os.path.join(ROIPATH, roi+"_26.nii.gz"),
        os.path.join(ROIPATH, roi+"_27.nii.gz"),
        os.path.join(ROIPATH, roi+"_28.nii.gz")]


def get_RT_metadata_paths():
    return [
        os.path.join(METAPATH, "trtime_fh009_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh011_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh013_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh014_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh015_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh017_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh019_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh021_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh023_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh024_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh025_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh026_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh027_RT_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh028_RT_corr_EF.csv")]
        

def get_motor_metadata_paths():
    return [
        os.path.join(METAPATH, "trtime_fh009_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh011_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh013_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh014_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh015_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh017_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh019_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh021_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh023_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh024_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh025_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh026_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh027_motor_EF.csv"),
        os.path.join(METAPATH, "trtime_fh028_motor_EF.csv")]


def get_noise_metadata_paths():
    return [
        os.path.join(METAPATH, "trtime_fh009_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh011_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh013_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh014_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh015_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh017_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh019_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh021_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh023_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh024_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh025_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh026_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh027_noise_corr_EF.csv"),
        os.path.join(METAPATH, "trtime_fh028_noise_corr_EF.csv")]
