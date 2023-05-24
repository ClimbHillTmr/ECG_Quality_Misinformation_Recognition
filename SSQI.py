import numpy as np

def ecg_quality_assessment(ecg_signal, fs):
    # Calculate SQIkur
    mean = np.mean(ecg_signal)
    std = np.std(ecg_signal)
    n = len(ecg_signal)
    sqikur = np.sum(((ecg_signal - mean) / std) ** 4) / n

    # Calculate SQIsnr
    signal_variance = np.var(ecg_signal)
    absolute_signal = np.abs(ecg_signal)
    noise_variance = np.var(absolute_signal)
    sqisnr = signal_variance / noise_variance

    # Calculate SQIhos
    sqiskew = np.sum(((ecg_signal - np.mean(ecg_signal)) / np.std(ecg_signal)) ** 3) / len(ecg_signal)
    sqihos = np.abs(sqiskew) * (sqikur / 5)

    # Calculate SQI_p_
    f, pxx = welch(ecg_signal, fs=fs)
    qrs_power = np.trapz(pxx[(f >= 5) & (f <= 15)])
    total_power = np.trapz(pxx)
    sqi_p = qrs_power / total_power

    # Quality assessment
    if 0.5 < sqi_p < 0.8 and -0.8 < sqihos <= 0.8 and sqisnr > 10 and sqikur > 5:
        quality = "Good"
    else:
        quality = "Poor"

    return quality