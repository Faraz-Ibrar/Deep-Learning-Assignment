import { motion } from 'framer-motion';
import { Sparkles, Search } from 'lucide-react';
import { useState } from 'react';

// All 50 action classes with emojis and gradient colors
const actions = [
    { name: 'ApplyEyeMakeup', emoji: '💄', color: 'from-pink-400 to-rose-500' },
    { name: 'ApplyLipstick', emoji: '💋', color: 'from-red-400 to-pink-500' },
    { name: 'Archery', emoji: '🏹', color: 'from-green-500 to-teal-600' },
    { name: 'BabyCrawling', emoji: '👶', color: 'from-yellow-300 to-amber-400' },
    { name: 'BalanceBeam', emoji: '🤸‍♀️', color: 'from-purple-400 to-violet-500' },
    { name: 'BandMarching', emoji: '🎺', color: 'from-red-500 to-orange-500' },
    { name: 'BaseballPitch', emoji: '⚾', color: 'from-red-400 to-rose-500' },
    { name: 'Basketball', emoji: '🏀', color: 'from-orange-400 to-amber-500' },
    { name: 'BasketballDunk', emoji: '🏀', color: 'from-orange-500 to-red-500' },
    { name: 'BenchPress', emoji: '🏋️', color: 'from-slate-500 to-gray-600' },
    { name: 'Biking', emoji: '🚴', color: 'from-green-400 to-emerald-500' },
    { name: 'Billiards', emoji: '🎱', color: 'from-green-600 to-emerald-700' },
    { name: 'BlowDryHair', emoji: '💇', color: 'from-pink-300 to-purple-400' },
    { name: 'BlowingCandles', emoji: '🎂', color: 'from-yellow-400 to-orange-400' },
    { name: 'Bowling', emoji: '🎳', color: 'from-blue-400 to-indigo-500' },
    { name: 'BoxingPunchingBag', emoji: '🥊', color: 'from-red-500 to-red-600' },
    { name: 'BoxingSpeedBag', emoji: '🥊', color: 'from-red-400 to-orange-500' },
    { name: 'BreastStroke', emoji: '🏊', color: 'from-cyan-400 to-blue-500' },
    { name: 'BrushingTeeth', emoji: '🪥', color: 'from-blue-300 to-cyan-400' },
    { name: 'CleanAndJerk', emoji: '🏋️‍♂️', color: 'from-gray-500 to-slate-600' },
    { name: 'CliffDiving', emoji: '🤿', color: 'from-blue-500 to-indigo-600' },
    { name: 'CricketBowling', emoji: '🏏', color: 'from-green-500 to-lime-600' },
    { name: 'CricketShot', emoji: '🏏', color: 'from-lime-500 to-green-600' },
    { name: 'Diving', emoji: '🏊‍♂️', color: 'from-blue-400 to-cyan-500' },
    { name: 'Drumming', emoji: '🥁', color: 'from-purple-400 to-violet-500' },
    { name: 'Fencing', emoji: '🤺', color: 'from-gray-400 to-slate-500' },
    { name: 'FloorGymnastics', emoji: '🤸', color: 'from-pink-400 to-purple-500' },
    { name: 'FrisbeeCatch', emoji: '🥏', color: 'from-yellow-400 to-lime-500' },
    { name: 'GolfSwing', emoji: '⛳', color: 'from-green-400 to-teal-500' },
    { name: 'Haircut', emoji: '✂️', color: 'from-amber-400 to-orange-500' },
    { name: 'Hammering', emoji: '🔨', color: 'from-amber-500 to-yellow-600' },
    { name: 'HandstandPushups', emoji: '🤸‍♂️', color: 'from-indigo-400 to-purple-500' },
    { name: 'HighJump', emoji: '🦘', color: 'from-blue-400 to-violet-500' },
    { name: 'HorseRiding', emoji: '🐎', color: 'from-amber-400 to-yellow-500' },
    { name: 'HulaHoop', emoji: '⭕', color: 'from-pink-400 to-rose-400' },
    { name: 'IceDancing', emoji: '⛸️', color: 'from-cyan-300 to-blue-400' },
    { name: 'JavelinThrow', emoji: '🎯', color: 'from-orange-400 to-red-500' },
    { name: 'JugglingBalls', emoji: '🤹', color: 'from-purple-400 to-pink-500' },
    { name: 'JumpingJack', emoji: '🏃', color: 'from-blue-400 to-cyan-500' },
    { name: 'Kayaking', emoji: '🚣', color: 'from-teal-400 to-cyan-500' },
    { name: 'Knitting', emoji: '🧶', color: 'from-rose-400 to-pink-500' },
    { name: 'LongJump', emoji: '🏃‍♂️', color: 'from-emerald-400 to-green-500' },
    { name: 'Lunges', emoji: '🦵', color: 'from-violet-400 to-purple-500' },
    { name: 'MoppingFloor', emoji: '🧹', color: 'from-blue-300 to-slate-400' },
    { name: 'ParallelBars', emoji: '🤸‍♀️', color: 'from-indigo-400 to-blue-500' },
    { name: 'PlayingGuitar', emoji: '🎸', color: 'from-indigo-400 to-purple-500' },
    { name: 'PlayingPiano', emoji: '🎹', color: 'from-gray-500 to-slate-600' },
    { name: 'PlayingViolin', emoji: '🎻', color: 'from-amber-500 to-orange-600' },
    { name: 'PushUps', emoji: '💪', color: 'from-red-400 to-rose-500' },
    { name: 'Skiing', emoji: '⛷️', color: 'from-sky-400 to-blue-500' },
];

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: {
            staggerChildren: 0.03,
        },
    },
};

const itemVariants = {
    hidden: { opacity: 0, y: 20, scale: 0.9 },
    visible: {
        opacity: 1,
        y: 0,
        scale: 1,
        transition: {
            type: 'spring',
            stiffness: 100,
            damping: 10,
        }
    },
};

export default function SupportedActionsGrid() {
    const [searchQuery, setSearchQuery] = useState('');

    const filteredActions = actions.filter(action =>
        action.name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <section className="py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5 }}
                    className="text-center mb-10"
                >
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-100/50 text-primary-700 text-sm font-medium mb-4">
                        <Sparkles className="w-4 h-4" />
                        <span>AI-Powered Classification</span>
                    </div>
                    <h2 className="text-3xl font-bold text-gray-900 mb-3">
                        Supported Actions
                    </h2>
                    <p className="text-gray-600 max-w-2xl mx-auto mb-6">
                        Our model can recognize <span className="font-semibold text-primary-600">50 action classes</span> from the UCF101 dataset.
                        Upload an image to see which action is being performed.
                    </p>

                    {/* Search Bar */}
                    <div className="max-w-md mx-auto relative">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Search actions..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="w-full pl-12 pr-4 py-3 rounded-xl border border-gray-200 bg-white/80 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200 text-gray-700 placeholder-gray-400"
                        />
                    </div>
                </motion.div>

                <motion.div
                    variants={containerVariants}
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true }}
                    className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 lg:grid-cols-6 xl:grid-cols-8 gap-3"
                >
                    {filteredActions.map((action, index) => (
                        <motion.div
                            key={action.name}
                            variants={itemVariants}
                            whileHover={{
                                scale: 1.05,
                                y: -5,
                                transition: { type: 'spring', stiffness: 300, damping: 15 }
                            }}
                            className="action-card group"
                        >
                            <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${action.color} flex items-center justify-center mb-2 shadow-md group-hover:shadow-lg transition-shadow duration-300`}>
                                <span className="text-xl">{action.emoji}</span>
                            </div>
                            <div className="flex items-center gap-1.5 mb-0.5">
                                <span className="text-[10px] font-bold text-gray-400">#{index + 1}</span>
                            </div>
                            <h3 className="font-medium text-gray-800 text-xs leading-tight">
                                {action.name.replace(/([A-Z])/g, ' $1').trim()}
                            </h3>
                        </motion.div>
                    ))}
                </motion.div>

                {filteredActions.length === 0 && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="text-center py-12 text-gray-500"
                    >
                        <p>No actions found matching "{searchQuery}"</p>
                    </motion.div>
                )}

                {/* Stats */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.5, delay: 0.3 }}
                    className="mt-8 flex justify-center gap-8 text-center"
                >
                    <div className="px-6 py-4 rounded-2xl bg-gradient-to-br from-primary-50 to-white border border-primary-100 shadow-sm">
                        <div className="text-3xl font-bold text-primary-600">50</div>
                        <div className="text-sm text-gray-600">Action Classes</div>
                    </div>
                    <div className="px-6 py-4 rounded-2xl bg-gradient-to-br from-green-50 to-white border border-green-100 shadow-sm">
                        <div className="text-3xl font-bold text-green-600">95%+</div>
                        <div className="text-sm text-gray-600">Avg. Accuracy</div>
                    </div>
                    <div className="px-6 py-4 rounded-2xl bg-gradient-to-br from-purple-50 to-white border border-purple-100 shadow-sm">
                        <div className="text-3xl font-bold text-purple-600">UCF101</div>
                        <div className="text-sm text-gray-600">Dataset</div>
                    </div>
                </motion.div>
            </div>
        </section>
    );
}

export { actions };
