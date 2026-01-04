import { Brain, Sparkles, Zap } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Header() {
    return (
        <header className="relative overflow-hidden py-16 lg:py-24">
            {/* Background Effects */}
            <div className="absolute inset-0 gradient-bg opacity-5"></div>
            <div className="hero-gradient absolute inset-0"></div>

            {/* Floating Orbs */}
            <div className="floating-orb w-96 h-96 bg-primary-500 -top-48 -left-48" style={{ animationDelay: '0s' }}></div>
            <div className="floating-orb w-64 h-64 bg-purple-500 top-20 -right-32" style={{ animationDelay: '2s' }}></div>
            <div className="floating-orb w-48 h-48 bg-pink-500 bottom-0 left-1/3" style={{ animationDelay: '4s' }}></div>

            <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                    className="mb-6"
                >
                    <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-primary-500 to-purple-600 shadow-2xl shadow-primary-500/30 mb-6">
                        <Brain className="w-10 h-10 text-white" />
                    </div>
                </motion.div>

                <motion.h1
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.1 }}
                    className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-gray-900 mb-6 leading-tight"
                >
                    AI Action{' '}
                    <span className="gradient-text">Recognition</span>{' '}
                    System
                </motion.h1>

                <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.2 }}
                    className="text-lg sm:text-xl text-gray-600 max-w-3xl mx-auto mb-8 leading-relaxed"
                >
                    Upload an image and let our powerful AI identify the action being performed.
                    Powered by advanced deep learning with CNN-LSTM architecture.
                </motion.p>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.3 }}
                    className="flex flex-wrap items-center justify-center gap-4"
                >
                    <div className="model-badge">
                        <Sparkles className="w-4 h-4" />
                        <span>CNN-LSTM Architecture</span>
                    </div>
                    <div className="model-badge">
                        <Zap className="w-4 h-4" />
                        <span>UCF101 Dataset</span>
                    </div>
                    <div className="model-badge">
                        <Brain className="w-4 h-4" />
                        <span>10 Action Classes</span>
                    </div>
                </motion.div>
            </div>
        </header>
    );
}
