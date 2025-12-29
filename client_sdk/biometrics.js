/**
 * Sentinel Fortress - Behavioral Biometrics SDK
 * Captures micro-behaviors (gyroscope, touch pressure, typing cadence)
 * to generate a "Liveness Score" for Zero-Trust Authentication.
 */

class SentinelBiometrics {
  constructor() {
    this.telemetry = {
      keystrokes: [],
      touchEvents: [],
      sensorData: [],
    };
    this.initSensors();
    this.initListeners();
  }

  initSensors() {
    if (window.DeviceOrientationEvent) {
      window.addEventListener('deviceorientation', (event) => {
        // Capture gyro wobble (indicative of human holding phone)
        this.telemetry.sensorData.push({
          type: 'gyro',
          alpha: event.alpha.toFixed(2),
          beta: event.beta.toFixed(2),
          gamma: event.gamma.toFixed(2),
          timestamp: Date.now()
        });
      });
    }

    if (window.DeviceMotionEvent) {
      window.addEventListener('devicemotion', (event) => {
        this.telemetry.sensorData.push({
          type: 'accel',
          x: event.acceleration.x?.toFixed(2),
          y: event.acceleration.y?.toFixed(2),
          z: event.acceleration.z?.toFixed(2),
          timestamp: Date.now()
        });
      });
    }
  }

  initListeners() {
    // Capture Typing Cadence (Flight time & Dwell time)
    document.addEventListener('keydown', (e) => {
      this.telemetry.keystrokes.push({
        key: e.key,
        event: 'down',
        timestamp: Date.now()
      });
    });

    document.addEventListener('keyup', (e) => {
      this.telemetry.keystrokes.push({
        key: e.key,
        event: 'up',
        timestamp: Date.now()
      });
    });

    // Capture Touch Pressure (if available) & Surface Area
    document.addEventListener('touchstart', (e) => {
      const touch = e.touches[0];
      this.telemetry.touchEvents.push({
        event: 'start',
        force: touch.force || 0, // Pressure (0-1)
        radiusX: touch.radiusX || 0,
        radiusY: touch.radiusY || 0,
        timestamp: Date.now()
      });
    });
  }

  /**
   * Returns the vectorized biometric payload for the Transaction Header.
   * Resets the buffer after collection to save memory.
   */
  getPayload() {
    const payload = {
      metrics: {
        gyro_variance: this.calculateVariance(this.telemetry.sensorData.filter(d => d.type === 'gyro')),
        typing_cadence_mean: this.calculateTypingCadence(),
        touch_pressure_avg: this.calculateAveragePressure(),
      },
      raw_sample_count: this.telemetry.sensorData.length,
      timestamp: Date.now()
    };

    // Reset buffers
    this.telemetry.keystrokes = [];
    this.telemetry.touchEvents = [];
    this.telemetry.sensorData = [];

    return JSON.stringify(payload);
  }

  calculateVariance(data) {
    if (data.length < 2) return 0;
    // Simple mock variance calc for beta (tilt front/back)
    const values = data.map(d => parseFloat(d.beta));
    const mean = values.reduce((a, b) => a + b, 0) / values.length;
    return values.reduce((t, n) => t + Math.pow(n - mean, 2), 0) / values.length;
  }

  calculateTypingCadence() {
    // Calculate average time between KeyDown and KeyUp
    const downEvents = {};
    let durations = [];
    
    this.telemetry.keystrokes.forEach(k => {
      if (k.event === 'down') {
        downEvents[k.key] = k.timestamp;
      } else if (k.event === 'up' && downEvents[k.key]) {
        durations.push(k.timestamp - downEvents[k.key]);
        delete downEvents[k.key];
      }
    });

    if (durations.length === 0) return 0;
    return durations.reduce((a, b) => a + b, 0) / durations.length;
  }

  calculateAveragePressure() {
    if (this.telemetry.touchEvents.length === 0) return 0;
    const total = this.telemetry.touchEvents.reduce((a, b) => a + b.force, 0);
    return total / this.telemetry.touchEvents.length;
  }
}

// Attach to window for global access
window.SentinelBiometrics = new SentinelBiometrics();
