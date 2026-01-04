import { useState, useCallback, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Upload,
    Image as ImageIcon,
    X,
    FileImage,
    CheckCircle2,
    AlertCircle
} from 'lucide-react';
import clsx from 'clsx';

const ACCEPTED_FORMATS = ['image/jpeg', 'image/jpg', 'image/png', 'image/jfif', 'image/avif'];
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

export default function ImageUpload({
    onImageUpload,
    uploadedImage,
    imagePreviewUrl,
    onClear,
    isLoading,
    error
}) {
    const [isDragging, setIsDragging] = useState(false);
    const [uploadError, setUploadError] = useState(null);
    const fileInputRef = useRef(null);

    const validateFile = useCallback((file) => {
        if (!file) return 'No file selected';

        // Check file type
        const fileType = file.type.toLowerCase();
        const fileName = file.name.toLowerCase();
        const validExtensions = ['.jpg', '.jpeg', '.png', '.jfif', '.avif'];
        const hasValidExtension = validExtensions.some(ext => fileName.endsWith(ext));

        if (!ACCEPTED_FORMATS.includes(fileType) && !hasValidExtension) {
            return 'Please upload a valid image file (JPG, PNG, JFIF, AVIF)';
        }

        // Check file size
        if (file.size > MAX_FILE_SIZE) {
            return 'Image must be under 10MB';
        }

        return null;
    }, []);

    const handleFile = useCallback((file) => {
        const error = validateFile(file);
        if (error) {
            setUploadError(error);
            return;
        }

        setUploadError(null);
        onImageUpload(file);
    }, [validateFile, onImageUpload]);

    const handleDragEnter = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(true);
    }, []);

    const handleDragLeave = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
    }, []);

    const handleDragOver = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
    }, []);

    const handleDrop = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);

        const files = e.dataTransfer.files;
        if (files && files.length > 0) {
            handleFile(files[0]);
        }
    }, [handleFile]);

    const handleClick = () => {
        fileInputRef.current?.click();
    };

    const handleFileChange = (e) => {
        const file = e.target.files?.[0];
        if (file) {
            handleFile(file);
        }
    };

    const displayError = uploadError || error;

    return (
        <div className="w-full">
            <input
                ref={fileInputRef}
                type="file"
                accept=".jpg,.jpeg,.png,.jfif,.avif,image/jpeg,image/png,image/avif"
                onChange={handleFileChange}
                className="hidden"
                aria-label="Upload image file"
            />

            <AnimatePresence mode="wait">
                {!imagePreviewUrl ? (
                    <motion.div
                        key="upload-zone"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className={clsx(
                            'upload-zone p-8',
                            isDragging && 'dragging',
                            isLoading && 'opacity-50 pointer-events-none'
                        )}
                        onDragEnter={handleDragEnter}
                        onDragLeave={handleDragLeave}
                        onDragOver={handleDragOver}
                        onDrop={handleDrop}
                        onClick={handleClick}
                        role="button"
                        tabIndex={0}
                        aria-label="Click or drag to upload image"
                        onKeyPress={(e) => e.key === 'Enter' && handleClick()}
                    >
                        <motion.div
                            initial={{ scale: 0.8, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            transition={{ delay: 0.1 }}
                            className="text-center"
                        >
                            <div className="relative mb-6">
                                <div className="w-20 h-20 mx-auto rounded-2xl bg-gradient-to-br from-primary-100 to-purple-100 flex items-center justify-center">
                                    <Upload className="w-10 h-10 text-primary-500" />
                                </div>
                                {isDragging && (
                                    <motion.div
                                        initial={{ scale: 0.8, opacity: 0 }}
                                        animate={{ scale: 1, opacity: 1 }}
                                        className="absolute inset-0 flex items-center justify-center"
                                    >
                                        <div className="w-24 h-24 rounded-2xl bg-primary-500/20 border-2 border-primary-500 animate-pulse"></div>
                                    </motion.div>
                                )}
                            </div>

                            <h3 className="text-xl font-semibold text-gray-800 mb-2">
                                {isDragging ? 'Drop your image here!' : 'Drag & drop an image here'}
                            </h3>
                            <p className="text-gray-500 mb-4">or</p>
                            <button
                                className="btn-primary mb-6"
                                onClick={(e) => {
                                    e.stopPropagation();
                                    handleClick();
                                }}
                            >
                                <span className="flex items-center gap-2">
                                    <FileImage className="w-5 h-5" />
                                    Browse Files
                                </span>
                            </button>

                            <div className="flex items-center justify-center gap-2 text-sm text-gray-400">
                                <ImageIcon className="w-4 h-4" />
                                <span>Supports: JPG, PNG, JFIF, AVIF (max 10MB)</span>
                            </div>
                        </motion.div>
                    </motion.div>
                ) : (
                    <motion.div
                        key="preview"
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        className="upload-zone has-image p-4"
                    >
                        <div className="relative w-full">
                            <div className="relative rounded-xl overflow-hidden bg-gray-100">
                                <img
                                    src={imagePreviewUrl}
                                    alt="Uploaded preview"
                                    className="w-full h-auto max-h-[400px] object-contain mx-auto"
                                />

                                {/* Success Badge */}
                                <div className="absolute top-4 left-4">
                                    <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-success-500/90 backdrop-blur-sm text-white text-sm font-medium shadow-lg">
                                        <CheckCircle2 className="w-4 h-4" />
                                        <span>Image Uploaded</span>
                                    </div>
                                </div>

                                {/* File Info */}
                                <div className="absolute bottom-4 left-4 right-4">
                                    <div className="glass-card rounded-lg p-3 flex items-center justify-between">
                                        <div className="flex items-center gap-3">
                                            <div className="w-10 h-10 rounded-lg bg-primary-100 flex items-center justify-center">
                                                <ImageIcon className="w-5 h-5 text-primary-600" />
                                            </div>
                                            <div>
                                                <p className="text-sm font-medium text-gray-800 truncate max-w-[200px]">
                                                    {uploadedImage?.name}
                                                </p>
                                                <p className="text-xs text-gray-500">
                                                    {(uploadedImage?.size / 1024).toFixed(1)} KB
                                                </p>
                                            </div>
                                        </div>

                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                onClear();
                                            }}
                                            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                                            aria-label="Clear uploaded image"
                                            disabled={isLoading}
                                        >
                                            <X className="w-5 h-5 text-gray-500" />
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Error Message */}
            <AnimatePresence>
                {displayError && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="mt-4 p-4 rounded-xl bg-danger-500/10 border border-danger-200 flex items-center gap-3"
                    >
                        <AlertCircle className="w-5 h-5 text-danger-500 flex-shrink-0" />
                        <p className="text-sm text-danger-600">{displayError}</p>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
