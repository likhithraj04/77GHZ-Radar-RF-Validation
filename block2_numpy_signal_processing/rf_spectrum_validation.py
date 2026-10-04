"""
Block 2 - NumPy + I/Q + FFT + Signal Processing
77-GHz Automotive Radar RF Validation

Educational example only. RF limits and signal values are illustrative.
"""

import numpy as np
from scipy.signal import find_peaks

FS_HZ = 20e6
N_SAMPLES = 2000
SPUR_LIMIT_DBC = -45.0
NOISE_BAND_LOW_HZ = 6e6
NOISE_BAND_HIGH_HZ = 8e6
PROMINENCE_FACTOR = 5.0


def generate_test_iq(fs_hz, n_samples):
    """Generate illustrative complex I/Q measurement data."""
    time_s = np.arange(n_samples) / fs_hz

    main_signal = np.exp(1j * 2 * np.pi * 2e6 * time_s)
    spur_1 = 0.01 * np.exp(1j * 2 * np.pi * 2.5e6 * time_s)
    spur_2 = 0.003 * np.exp(1j * 2 * np.pi * 4e6 * time_s)

    noise = (
        np.random.randn(n_samples)
        + 1j * np.random.randn(n_samples)
    ) * 0.0005

    signal = main_signal + spur_1 + spur_2 + noise

    return time_s, np.real(signal), np.imag(signal)


def calculate_spectrum(signal, fs_hz):
    """Convert complex I/Q data into frequency-domain magnitude."""
    n_samples = len(signal)

    spectrum = np.fft.fft(signal)
    frequency_hz = np.fft.fftfreq(n_samples, 1 / fs_hz)
    magnitude = np.abs(spectrum)

    return frequency_hz, magnitude


def estimate_noise_floor(frequency_hz, magnitude, low_hz, high_hz):
    """Estimate a simple relative FFT-magnitude noise floor."""
    mask = (frequency_hz >= low_hz) & (frequency_hz <= high_hz)
    samples = magnitude[mask]

    if len(samples) == 0:
        raise ValueError("Noise estimation band contains no FFT bins.")

    return float(np.median(samples))


def detect_spectral_peaks(magnitude, noise_floor, prominence_factor):
    """Detect peaks using SciPy find_peaks()."""
    prominence = prominence_factor * noise_floor

    peaks, _ = find_peaks(
        magnitude,
        prominence=prominence
    )

    return peaks


def identify_main_component(peaks, magnitude, frequency_hz):
    """Select the strongest detected spectral component."""
    if len(peaks) == 0:
        raise RuntimeError("No spectral peaks detected.")

    strongest_position = np.argmax(magnitude[peaks])
    main_index = int(peaks[strongest_position])

    return (
        main_index,
        float(frequency_hz[main_index]),
        float(magnitude[main_index])
    )


def calculate_spur_results(
    peaks,
    main_index,
    frequency_hz,
    magnitude,
    spur_limit_dbc
):
    """Calculate dBc and PASS/FAIL for every non-main peak."""
    results = []

    for index in peaks[peaks != main_index]:
        spur_magnitude = float(magnitude[index])

        spur_dbc = 20 * np.log10(
            spur_magnitude / magnitude[main_index]
        )

        results.append({
            "index": int(index),
            "frequency_hz": float(frequency_hz[index]),
            "magnitude": spur_magnitude,
            "spur_dbc": float(spur_dbc),
            "status": "PASS" if spur_dbc <= spur_limit_dbc else "FAIL"
        })

    return results


def print_report(main_frequency_hz, noise_floor, spur_results):
    """Print the RF spectral validation report."""
    print("\n" + "=" * 68)
    print("       77 GHz RADAR TX SPECTRAL VALIDATION")
    print("=" * 68)

    print(f"\nMain component : {main_frequency_hz / 1e6:.3f} MHz")
    print(
        f"Noise floor    : "
        f"{20 * np.log10(noise_floor):.2f} dB "
        f"(relative FFT magnitude)"
    )
    print(f"Spur limit     : {SPUR_LIMIT_DBC:.1f} dBc")

    print("\n" + "-" * 68)
    print(f"{'Frequency':>14} | {'Spur Level':>12} | {'Status':>8}")
    print("-" * 68)

    overall_pass = True

    if not spur_results:
        print("No spurs detected.")
    else:
        for result in spur_results:
            print(
                f"{result['frequency_hz'] / 1e6:>11.3f} MHz | "
                f"{result['spur_dbc']:>9.2f} dBc | "
                f"{result['status']:>8}"
            )

            if result["status"] == "FAIL":
                overall_pass = False

    print("-" * 68)
    print("Overall Test: PASS" if overall_pass else "Overall Test: FAIL")
    print("=" * 68)


def main():
    """Execute the complete Block 2 spectral-validation case."""
    print("\nStarting Block 2 RF spectral validation...")

    _, i_signal, q_signal = generate_test_iq(
        FS_HZ,
        N_SAMPLES
    )

    complex_signal = i_signal + 1j * q_signal

    frequency_hz, magnitude = calculate_spectrum(
        complex_signal,
        FS_HZ
    )

    noise_floor = estimate_noise_floor(
        frequency_hz,
        magnitude,
        NOISE_BAND_LOW_HZ,
        NOISE_BAND_HIGH_HZ
    )

    peaks = detect_spectral_peaks(
        magnitude,
        noise_floor,
        PROMINENCE_FACTOR
    )

    main_index, main_frequency_hz, _ = identify_main_component(
        peaks,
        magnitude,
        frequency_hz
    )

    spur_results = calculate_spur_results(
        peaks,
        main_index,
        frequency_hz,
        magnitude,
        SPUR_LIMIT_DBC
    )

    print_report(
        main_frequency_hz,
        noise_floor,
        spur_results
    )

    print("\nTest execution completed.\n")


if __name__ == "__main__":
    main()
