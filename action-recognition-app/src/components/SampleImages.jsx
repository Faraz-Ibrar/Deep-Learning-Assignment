import { motion } from 'framer-motion';
import { ImageIcon, Sparkles } from 'lucide-react';

// Sample image URLs from Unsplash (free to use)
const sampleImages = [
    {
        id: 1,
        url: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop',
        action: 'Biking',
        alt: 'Person biking outdoors'
    },
    {
        id: 2,
        url: 'https://images.unsplash.com/photo-1520341280432-4749d4d7bcf9?w=400&h=300&fit=crop',
        action: 'Basketball',
        alt: 'Person playing basketball'
    },
    {
        id: 3,
        url: 'https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=400&h=300&fit=crop',
        action: 'PlayingGuitar',
        alt: 'Person playing guitar'
    },
    {
        id: 4,
        url: 'https://images.unsplash.com/photo-1530549387789-4c1017266635?w=400&h=300&fit=crop',
        action: 'Swimming',
        alt: 'Person swimming in pool'
    },
];

export default function SampleImages({ onSampleSelect, disabled }) {
    const handleSampleClick = async (sample) => {
        if (disabled) return;

        try {
            // Fetch the image and convert to File object
            const response = await fetch(sample.url);
            const blob = await response.blob();
            const file = new File([blob], `sample-${sample.action.toLowerCase()}.jpg`, { type: 'image/jpeg' });
            onSampleSelect(file);
        } catch (error) {
            console.error('Failed to load sample image:', error);
        }
    };

    return (
        <section className="py-8 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-transparent to-gray-50/50">
            <div className="max-w-6xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    className="text-center mb-8"
                >
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-100/50 text-purple-700 text-sm font-medium mb-4">
                        <Sparkles className="w-4 h-4" />
                        <span>Quick Start</span>
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">
                        Try Sample Images
                    </h2>
                    <p className="text-gray-600">
                        Click on any sample image below to see the AI in action
                    </p>
                </motion.div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {sampleImages.map((sample, index) => (
                        <motion.button
                            key={sample.id}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: index * 0.1 }}
                            whileHover={{ scale: 1.03, y: -5 }}
                            whileTap={{ scale: 0.98 }}
                            onClick={() => handleSampleClick(sample)}
                            disabled={disabled}
                            className="relative group rounded-xl overflow-hidden aspect-[4/3] bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <img
                                src={sample.url}
                                alt={sample.alt}
                                className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                                loading="lazy"
                            />
                            <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                                <div className="absolute bottom-0 left-0 right-0 p-4">
                                    <p className="text-white font-semibold">{sample.action}</p>
                                    <p className="text-white/70 text-sm">Click to try</p>
                                </div>
                            </div>
                            <div className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                                <div className="w-8 h-8 rounded-full bg-white/90 flex items-center justify-center shadow-lg">
                                    <ImageIcon className="w-4 h-4 text-gray-700" />
                                </div>
                            </div>
                        </motion.button>
                    ))}
                </div>
            </div>
        </section>
    );
}
