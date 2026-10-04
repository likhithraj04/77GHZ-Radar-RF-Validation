# Block 2 — NumPy + I/Q + FFT + Signal Processing

## 77-GHz Automotive Radar RF Validation

This block extends the Block 1 RF validation framework into signal-level analysis.

### Engineering problem

The Python analysis takes complex I/Q data and:

1. Performs FFT processing.
2. Builds the frequency axis.
3. Identifies the main spectral component.
4. Estimates a relative noise floor.
5. Detects additional spectral peaks.
6. Calculates spur levels in dBc.
7. Compares spurs with the requirement.
8. Produces an overall PASS/FAIL result.

```text
I/Q data
   ↓
Complex signal
   ↓
FFT
   ↓
Frequency axis + magnitude
   ↓
Noise-floor estimation
   ↓
Peak detection
   ↓
Main component identification
   ↓
Spur detection
   ↓
dBc calculation
   ↓
Requirement check
   ↓
PASS / FAIL
```

> **Important:** RF values and limits in this training project are illustrative. They are not claimed product specifications or regulatory limits.

## Training case

| Component | Frequency | Relative amplitude |
|---|---:|---:|
| Main component | 2.000 MHz | 1.0 |
| Spur 1 | 2.500 MHz | 0.01 |
| Spur 2 | 4.000 MHz | 0.003 |
| Noise | Random | 0.0005 scale |

Sampling frequency = 20 MHz  
Number of samples = 2000  
Observation time = 100 us  
FFT bin spacing = Fs / N = 10 kHz

Illustrative requirement:

```text
Spur <= -45 dBc
```

## Concepts learned

### NumPy

- arrays
- complex arrays
- `np.arange()`
- `np.real()`
- `np.imag()`
- `np.abs()`
- `np.argmax()`
- Boolean masks
- `np.median()`
- `np.log10()`
- `np.fft.fft()`
- `np.fft.fftfreq()`

### I/Q

```python
I = np.real(signal)
Q = np.imag(signal)
complex_signal = I + 1j * Q
```

### FFT

```python
spectrum = np.fft.fft(signal)
```

### Frequency axis

```python
freq = np.fft.fftfreq(N, 1 / fs)
```

### Peak detection

```python
from scipy.signal import find_peaks

peaks, properties = find_peaks(
    magnitude,
    prominence=prominence_threshold
)
```

### dBc

For an amplitude/magnitude ratio:

```python
spur_dbc = 20 * np.log10(spur / carrier)
```

More negative dBc means a weaker spur.

## Prominence

Peak prominence describes how strongly a peak stands out from its surrounding baseline.

The example uses:

```python
prominence = 5 * noise_floor
```

This is an educational rule only. A production algorithm must validate the threshold against known-good data, injected spurs, SNR variation, FFT settings, windowing, expected components, and false-positive/false-negative behavior.

## Noise floor

The example estimates noise using a frequency region away from the expected signal components and uses the median.

This is a **relative FFT-domain estimate**, not automatically a calibrated dBm/Hz measurement.

Real RF measurements require consideration of:

- RBW
- detector mode
- averaging
- calibration
- FFT scaling
- windowing
- measurement bandwidth
- instrument noise floor

## Spectral leakage and windowing

Finite observation can cause spectral leakage when the signal does not contain an integer number of cycles inside the observation interval.

A Hann window can reduce sidelobes:

```python
window = np.hanning(N)
windowed_signal = signal * window
```

Windowing involves trade-offs such as lower sidelobes versus a wider main lobe and amplitude correction.

## Frequency resolution vs discrimination

FFT bin spacing is:

```text
Δf = Fs / N
```

It is not identical to frequency discrimination. Discrimination also depends on window main-lobe width, sidelobes, SNR, observation time, and signal characteristics.

## Engineering interpretation

If the analysis reports:

```text
2.500 MHz | -40 dBc | FAIL
4.000 MHz | -50 dBc | PASS
```

with a requirement of `<= -45 dBc`, the overall test fails.

Do not immediately declare the DUT defective. Investigate:

- DUT-generated spur
- PLL/clock coupling
- mixer products
- power-supply coupling
- EMI/external interference
- cable/connector problems
- instrument configuration
- signal-processing artifacts

## Measurement vs processing vs DUT failure

A professional validation engineer separates:

**Measurement problems**
- incorrect RBW
- calibration issue
- wrong span
- instrument overload
- cable-loss error
- trigger problem

**Processing problems**
- incorrect FFT scaling
- wrong frequency axis
- poor window selection
- bad noise region
- false peak detection

**DUT problems**
- PLL spur
- clock coupling
- power-supply coupling
- nonlinear behavior
- mixer product
- RF leakage

## Interview questions

**Why use complex I/Q data?**  
I/Q preserves amplitude and phase information and enables complex signal processing.

**How do you calculate FFT frequency resolution?**  
`Δf = Fs / N`.

**What is dBc?**  
A spectral level expressed relative to the carrier/main signal.

**Why is more negative dBc better for a spur?**  
Because the unwanted component is weaker relative to the carrier.

**What is spectral leakage?**  
Spreading of signal energy into neighboring FFT bins due to finite observation and boundary discontinuity.

**Why use a window?**  
To reduce spectral sidelobes/leakage, accepting trade-offs such as wider main lobe and amplitude correction.

**What is peak prominence?**  
A measure of how strongly a peak stands out from its surrounding baseline.

**Would you immediately declare a DUT failure after detecting a spur?**  
No. I would first verify the measurement setup, instrument configuration, calibration, processing, repeatability, and known-good DUT behavior.

## Block 2 status

**COMPLETE**

Next block:

# Block 3 — Matplotlib + Professional RF Spectrum Analysis

The next step is to turn the numerical analysis into engineering plots for RF debugging and validation.
