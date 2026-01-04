import { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Wand2, Loader2 } from 'lucide-react';

import Header from './components/Header';
import SupportedActionsGrid, { actions } from './components/SupportedActionsGrid';
import ImageUpload from './components/ImageUpload';
import PredictionResults from './components/PredictionResults';
import ModelInfo from './components/ModelInfo';
import SampleImages from './components/SampleImages';
import Footer from './components/Footer';

// API Configuration
const API_BASE_URL = 'http://localhost:8000';

/**
 * Send image to backend API for prediction
 * @param {File} imageFile - The image file to analyze
 * @returns {Promise<Array>} - Array of predictions with rank, action, confidence
 */
async function getPredictionFromAPI(imageFile) {
  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `API Error: ${response.status}`);
  }

  const data = await response.json();

  if (!data.success) {
    throw new Error('Prediction failed');
  }

  return data.predictions;
}

function App() {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [imagePreviewUrl, setImagePreviewUrl] = useState('');
  const [predictions, setPredictions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const processImage = useCallback((file) => {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        resolve(reader.result);
      };
      reader.readAsDataURL(file);
    });
  }, []);

  const handleImageUpload = useCallback(async (file) => {
    setError(null);
    setUploadedImage(file);

    try {
      // Create preview URL
      const previewUrl = await processImage(file);
      setImagePreviewUrl(previewUrl);

      // Start prediction
      setIsLoading(true);
      setPredictions([]);

      // Call the real API
      const apiPredictions = await getPredictionFromAPI(file);
      setPredictions(apiPredictions);

    } catch (err) {
      console.error('Prediction error:', err);
      if (err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
        setError('Cannot connect to the prediction server. Please ensure the backend is running on http://localhost:8000');
      } else {
        setError(err.message || 'Could not analyze image. Please try another.');
      }
    } finally {
      setIsLoading(false);
    }
  }, [processImage]);

  const handleClear = useCallback(() => {
    setUploadedImage(null);
    setImagePreviewUrl('');
    setPredictions([]);
    setError(null);
  }, []);

  const handleAnalyze = useCallback(async () => {
    if (!uploadedImage) return;

    setIsLoading(true);
    setPredictions([]);
    setError(null);

    try {
      // Call the real API
      const apiPredictions = await getPredictionFromAPI(uploadedImage);
      setPredictions(apiPredictions);
    } catch (err) {
      console.error('Prediction error:', err);
      if (err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
        setError('Cannot connect to the prediction server. Please ensure the backend is running on http://localhost:8000');
      } else {
        setError(err.message || 'Could not analyze image. Please try another.');
      }
    } finally {
      setIsLoading(false);
    }
  }, [uploadedImage]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <Header />

      <SupportedActionsGrid />

      {/* Main Content - Upload and Predictions */}
      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left Column - Upload */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="glass-card rounded-2xl p-6"
            >
              <h2 className="section-title">Upload Image</h2>

              <ImageUpload
                onImageUpload={handleImageUpload}
                uploadedImage={uploadedImage}
                imagePreviewUrl={imagePreviewUrl}
                onClear={handleClear}
                isLoading={isLoading}
                error={error}
              />

              {/* Analyze Button */}
              {imagePreviewUrl && predictions.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mt-6"
                >
                  <button
                    onClick={handleAnalyze}
                    disabled={isLoading}
                    className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="w-5 h-5 animate-spin" />
                        <span>Analyzing...</span>
                      </>
                    ) : (
                      <>
                        <Wand2 className="w-5 h-5" />
                        <span>Analyze Again</span>
                      </>
                    )}
                  </button>
                </motion.div>
              )}
            </motion.div>

            {/* Right Column - Predictions */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="glass-card rounded-2xl p-6"
            >
              <h2 className="section-title">Prediction Results</h2>

              <PredictionResults
                predictions={predictions}
                isLoading={isLoading}
              />
            </motion.div>
          </div>
        </div>
      </section>

      <SampleImages
        onSampleSelect={handleImageUpload}
        disabled={isLoading}
      />

      <ModelInfo />

      <Footer />
    </div>
  );
}

export default App;
