def ecg_quality_zhao2018(ecg, rpeaks=None, sampling_rate=500):
    if rpeaks is None:
        rpeaks = [
            i
            for i in range(1, len(ecg_data) - 1)
            if ecg_data[i] > ecg_data[i - 1] and ecg_data[i] > ecg_data[i + 1]
        ]
        rpeaks = np.array(rpeaks)

    # Calculate quality indices
    kurtosis = np.mean((ecg_data - np.mean(ecg_data)) ** 4) / np.mean((ecg_data - np.mean(ecg_data)) ** 2) ** 2
    pSQI = np.mean(ecg_data ** 2)
    basSQI = np.max(ecg_data) / np.mean(ecg_data)

    # Classify quality indices
    ecg_rate = 60000.0 / (1000.0 / sampling_rate * np.min(np.diff(rpeaks))) if len(rpeaks) > 1 else 1
    pSQI_class = 2 if (pSQI > 0.5 and ecg_rate < 130) or (pSQI > 0.8 and ecg_rate >= 130) else (1 if 0.4 < pSQI < 0.5 or 0.3 < pSQI < 0.4 else 0)
    kSQI_class = 2 if kurtosis > 5 else 0
    basSQI_class = 2 if basSQI >= 0.95 else (1 if 0.9 <= basSQI < 0.95 else 0)

    # Calculate final classification
    class_matrix = np.array([pSQI_class, kSQI_class, basSQI_class])
    n_optimal = np.sum(class_matrix == 2)
    n_suspicious = np.sum(class_matrix == 1)
    n_unqualified = np.sum(class_matrix == 0)

    if n_unqualified >= 2 or (n_unqualified == 1 and n_suspicious == 2):
        return "Unacceptable"
    elif n_optimal >= 2 and n_unqualified == 0:
        return "Excellent"
    else:
        return "Barely acceptable"