import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    ChevronDown,
    Database,
    Layers,
    Target,
    Cpu,
    Info
} from 'lucide-react';
import clsx from 'clsx';

const modelDetails = [
    {
        icon: Cpu,
        label: 'Model Architecture',
        value: 'CNN + LSTM',
        description: 'InceptionV3/MobileNetV2 backbone with LSTM temporal layers'
    },
    {
        icon: Database,
        label: 'Training Dataset',
        value: 'UCF101',
        description: 'University of Central Florida action recognition dataset'
    },
    {
        icon: Layers,
        label: 'Number of Classes',
        value: '10',
        description: 'Trained on a subset of 10 action categories'
    },
    {
        icon: Target,
        label: 'Test Accuracy',
        value: '~65%',
        description: 'Model accuracy on the test set (single frame)'
    },
];

export default function ModelInfo() {
    const [isExpanded, setIsExpanded] = useState(false);

    return (
        <section className="py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-6xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    className="glass-card rounded-2xl overflow-hidden"
                >
                    {/* Header - Always Visible */}
                    <button
                        onClick={() => setIsExpanded(!isExpanded)}
                        className="w-full p-6 flex items-center justify-between text-left hover:bg-gray-50/50 transition-colors"
                        aria-expanded={isExpanded}
                        aria-controls="model-info-content"
                    >
                        <div className="flex items-center gap-4">
                            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-500 to-purple-600 flex items-center justify-center">
                                <Info className="w-6 h-6 text-white" />
                            </div>
                            <div>
                                <h2 className="text-xl font-bold text-gray-900">Model Information</h2>
                                <p className="text-gray-500 text-sm">Learn about the AI model behind the predictions</p>
                            </div>
                        </div>
                        <motion.div
                            animate={{ rotate: isExpanded ? 180 : 0 }}
                            transition={{ duration: 0.3 }}
                            className="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center"
                        >
                            <ChevronDown className="w-5 h-5 text-gray-600" />
                        </motion.div>
                    </button>

                    {/* Expandable Content */}
                    <AnimatePresence>
                        {isExpanded && (
                            <motion.div
                                id="model-info-content"
                                initial={{ height: 0, opacity: 0 }}
                                animate={{ height: 'auto', opacity: 1 }}
                                exit={{ height: 0, opacity: 0 }}
                                transition={{ duration: 0.3 }}
                                className="overflow-hidden"
                            >
                                <div className="p-6 pt-0 border-t border-gray-100">
                                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-6">
                                        {modelDetails.map((detail, index) => (
                                            <motion.div
                                                key={detail.label}
                                                initial={{ opacity: 0, y: 10 }}
                                                animate={{ opacity: 1, y: 0 }}
                                                transition={{ delay: index * 0.1 }}
                                                className="p-4 rounded-xl bg-gray-50 hover:bg-gray-100 transition-colors"
                                            >
                                                <div className="flex items-start gap-4">
                                                    <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary-100 to-purple-100 flex items-center justify-center flex-shrink-0">
                                                        <detail.icon className="w-5 h-5 text-primary-600" />
                                                    </div>
                                                    <div>
                                                        <p className="text-sm text-gray-500 mb-1">{detail.label}</p>
                                                        <p className="font-bold text-gray-900">{detail.value}</p>
                                                        <p className="text-xs text-gray-400 mt-1">{detail.description}</p>
                                                    </div>
                                                </div>
                                            </motion.div>
                                        ))}
                                    </div>

                                    {/* Best Results Note */}
                                    <motion.div
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        transition={{ delay: 0.5 }}
                                        className="mt-6 p-4 rounded-xl bg-gradient-to-r from-green-50 to-emerald-50 border border-green-100"
                                    >
                                        <h4 className="font-semibold text-green-800 mb-2 flex items-center gap-2">
                                            <Target className="w-4 h-4" />
                                            Best Results For
                                        </h4>
                                        <div className="flex flex-wrap gap-2">
                                            {['Biking', 'HorseRiding', 'PlayingGuitar', 'Drumming', 'WritingOnBoard'].map((action) => (
                                                <span
                                                    key={action}
                                                    className="px-3 py-1 rounded-full bg-green-100 text-green-700 text-sm font-medium"
                                                >
                                                    {action}
                                                </span>
                                            ))}
                                        </div>
                                    </motion.div>
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </motion.div>
            </div>
        </section>
    );
}
