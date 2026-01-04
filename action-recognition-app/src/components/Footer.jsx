import { Brain, Github, Heart } from 'lucide-react';

export default function Footer() {
    return (
        <footer className="py-8 px-4 sm:px-6 lg:px-8 border-t border-gray-100">
            <div className="max-w-6xl mx-auto">
                <div className="flex flex-col md:flex-row items-center justify-between gap-4">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-purple-600 flex items-center justify-center">
                            <Brain className="w-5 h-5 text-white" />
                        </div>
                        <div>
                            <p className="font-semibold text-gray-800">AI Action Recognition</p>
                            <p className="text-sm text-gray-500">CNN-LSTM • UCF101 Dataset</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-2 text-gray-500 text-sm">
                        <span>Made with</span>
                        <Heart className="w-4 h-4 text-red-500 fill-red-500" />
                        <span>using React & TailwindCSS</span>
                    </div>

                    <div className="flex items-center gap-4">
                        <a
                            href="#"
                            className="text-gray-400 hover:text-gray-600 transition-colors"
                            aria-label="GitHub Repository"
                        >
                            <Github className="w-5 h-5" />
                        </a>
                    </div>
                </div>

                <div className="mt-6 pt-6 border-t border-gray-100 text-center">
                    <p className="text-sm text-gray-400">
                        © {new Date().getFullYear()} Action Recognition AI. For educational purposes only.
                    </p>
                </div>
            </div>
        </footer>
    );
}
