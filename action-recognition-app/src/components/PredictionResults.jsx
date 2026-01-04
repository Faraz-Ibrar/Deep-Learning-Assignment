import { motion } from 'framer-motion';
import {
    Trophy,
    TrendingUp,
    BarChart3,
    Sparkles,
    Info
} from 'lucide-react';
import clsx from 'clsx';
import { actions } from './SupportedActionsGrid';

function getConfidenceColor(confidence) {
    if (confidence >= 60) return { bg: 'bg-success-500', text: 'text-success-500', gradient: 'from-success-400 to-success-600' };
    if (confidence >= 40) return { bg: 'bg-warning-500', text: 'text-warning-500', gradient: 'from-warning-400 to-warning-600' };
    return { bg: 'bg-danger-500', text: 'text-danger-500', gradient: 'from-danger-400 to-danger-600' };
}

function getActionEmoji(actionName) {
    const action = actions.find(a => a.name === actionName);
    return action?.emoji || '🎯';
}

function PredictionBar({ rank, action, confidence, delay = 0 }) {
    const color = getConfidenceColor(confidence);
    const emoji = getActionEmoji(action);

    return (
        <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay }}
            className="flex items-center gap-4 py-3 px-4 rounded-xl bg-gray-50 hover:bg-gray-100 transition-colors"
        >
            <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-gray-200 text-sm font-bold text-gray-600">
                #{rank}
            </div>

            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center text-xl">
                {emoji}
            </div>

            <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-1">
                    <span className="font-medium text-gray-800 truncate">
                        {action.replace(/([A-Z])/g, ' $1').trim()}
                    </span>
                    <span className={clsx('font-semibold text-sm', color.text)}>
                        {confidence.toFixed(1)}%
                    </span>
                </div>
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                    <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${confidence}%` }}
                        transition={{ duration: 0.8, delay: delay + 0.2, ease: 'easeOut' }}
                        className={clsx('h-full rounded-full bg-gradient-to-r', color.gradient)}
                    />
                </div>
            </div>
        </motion.div>
    );
}

export default function PredictionResults({ predictions, isLoading }) {
    if (!predictions || predictions.length === 0) {
        return (
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="h-full flex flex-col items-center justify-center text-center p-8"
            >
                <div className="w-20 h-20 rounded-2xl bg-gray-100 flex items-center justify-center mb-4">
                    <BarChart3 className="w-10 h-10 text-gray-400" />
                </div>
                <h3 className="text-lg font-semibold text-gray-700 mb-2">
                    No Predictions Yet
                </h3>
                <p className="text-gray-500 max-w-xs">
                    Upload an image to see AI predictions for the action being performed.
                </p>
            </motion.div>
        );
    }

    if (isLoading) {
        return (
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="h-full flex flex-col items-center justify-center p-8"
            >
                <div className="relative mb-6">
                    <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary-500 to-purple-600 flex items-center justify-center animate-pulse">
                        <Sparkles className="w-10 h-10 text-white" />
                    </div>
                    <div className="absolute inset-0 rounded-2xl bg-primary-500/30 animate-ping"></div>
                </div>
                <h3 className="text-lg font-semibold text-gray-700 mb-2">
                    Analyzing Image...
                </h3>
                <p className="text-gray-500">
                    Our AI is identifying the action
                </p>
                <div className="mt-6 flex gap-2">
                    {[0, 1, 2].map((i) => (
                        <motion.div
                            key={i}
                            animate={{ scale: [1, 1.3, 1] }}
                            transition={{ duration: 0.6, delay: i * 0.2, repeat: Infinity }}
                            className="w-3 h-3 rounded-full bg-primary-500"
                        />
                    ))}
                </div>
            </motion.div>
        );
    }

    const topPrediction = predictions[0];
    const topColor = getConfidenceColor(topPrediction.confidence);
    const topEmoji = getActionEmoji(topPrediction.action);

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-6"
        >
            {/* Top Prediction Card */}
            <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
                className="top-prediction-card text-white"
            >
                <div className="absolute inset-0 overflow-hidden rounded-2xl">
                    <div className="shimmer absolute inset-0"></div>
                </div>

                <div className="relative">
                    <div className="flex items-center gap-2 mb-4">
                        <Trophy className="w-5 h-5 text-yellow-400" />
                        <span className="text-sm font-medium text-white/80">Top Prediction</span>
                    </div>

                    <div className="flex items-center gap-4 mb-4">
                        <div className="w-16 h-16 rounded-xl bg-white/20 backdrop-blur-sm flex items-center justify-center text-3xl">
                            {topEmoji}
                        </div>
                        <div>
                            <h2 className="text-2xl font-bold">
                                {topPrediction.action.replace(/([A-Z])/g, ' $1').trim()}
                            </h2>
                            <p className="text-white/70 text-sm">Most Likely Action</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-4">
                        <div className={clsx(
                            'px-4 py-2 rounded-lg font-bold text-lg',
                            topPrediction.confidence >= 60 ? 'bg-green-500/30 text-green-300' :
                                topPrediction.confidence >= 40 ? 'bg-yellow-500/30 text-yellow-300' :
                                    'bg-red-500/30 text-red-300'
                        )}>
                            {topPrediction.confidence.toFixed(1)}%
                        </div>
                        <div className="flex-1 h-3 bg-white/20 rounded-full overflow-hidden">
                            <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${topPrediction.confidence}%` }}
                                transition={{ duration: 1, delay: 0.3, ease: 'easeOut' }}
                                className={clsx('h-full rounded-full',
                                    topPrediction.confidence >= 60 ? 'bg-green-400' :
                                        topPrediction.confidence >= 40 ? 'bg-yellow-400' :
                                            'bg-red-400'
                                )}
                            />
                        </div>
                    </div>
                </div>
            </motion.div>

            {/* All Top 5 Predictions */}
            <div>
                <div className="flex items-center gap-2 mb-4">
                    <TrendingUp className="w-5 h-5 text-primary-500" />
                    <h3 className="font-semibold text-gray-800">Top 5 Predictions</h3>
                </div>

                <div className="space-y-2">
                    {predictions.slice(0, 5).map((pred, index) => (
                        <PredictionBar
                            key={pred.action}
                            rank={pred.rank}
                            action={pred.action}
                            confidence={pred.confidence}
                            delay={index * 0.1}
                        />
                    ))}
                </div>
            </div>

            {/* Info Note */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.8 }}
                className="p-4 rounded-xl bg-primary-50 border border-primary-100 flex gap-3"
            >
                <Info className="w-5 h-5 text-primary-500 flex-shrink-0 mt-0.5" />
                <div className="text-sm text-primary-800">
                    <p className="font-medium mb-1">Note about accuracy</p>
                    <p className="text-primary-600">
                        This model was trained on video sequences. Single images may have lower accuracy,
                        especially for motion-based actions like JumpingJack or Swimming.
                    </p>
                </div>
            </motion.div>
        </motion.div>
    );
}
