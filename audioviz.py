#!/usr/bin/env python
# This script converts audio files (MP3) into high-quality video visualizations.
# It creates a Full HD video featuring a scrolling waveform visualization of the
# audio signal. The output is a black background with a cyan waveform that moves
# from left to right, similar to professional audio editing software.
import argparse
import os
import tempfile

from pydub import AudioSegment
import cv2
import matplotlib.pyplot as plt
import numpy as np


hd_width = 1920
hd_height = 1080


def create_audio_visualization(input_audio, output_video, fps=30):
    """
    Creates a Full HD video visualization of an audio file's waveform.

    Args:
        input_audio (str): Path to input MP3 file
        output_video (str): Path for output video file
        fps (int): Frames per second for the output video
    """
    # Load audio file
    audio = AudioSegment.from_mp3(input_audio)

    # Convert audio to numpy array
    samples = np.array(audio.get_array_of_samples())

    # Calculate number of samples per frame
    samples_per_frame = len(samples) // (audio.duration_seconds * fps)

    # Create temporary directory for frames
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up the matplotlib figure with full HD dimensions
        dpi = 100
        width_inches = hd_width / dpi
        height_inches = hd_height / dpi
        fig = plt.figure(figsize=(width_inches, height_inches), dpi=dpi)
        ax = fig.add_subplot(111)

        # Style settings
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')

        # Function to update the plot for each frame
        def save_frame(frame_number):
            ax.clear()

            # Calculate the window of samples for this frame
            start = int(frame_number * samples_per_frame)
            end = int(start + samples_per_frame * 60)  # Show ~2 seconds of audio

            # Get the audio data for this window
            if end >= len(samples):
                end = len(samples)
            data = samples[start:end]

            # Plot the waveform
            ax.plot(data, color='cyan', linewidth=1.5)

            # Set axis properties
            ax.set_ylim(-32768, 32768)
            ax.axis('off')

            # Ensure the plot fills the figure
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

            # Save the frame with exact dimensions
            frame_path = os.path.join(temp_dir, f'frame_{frame_number:05d}.png')
            fig.savefig(frame_path, dpi=dpi, bbox_inches='tight', pad_inches=0)
            return frame_path

        # Calculate total number of frames
        total_frames = int(audio.duration_seconds * fps)

        # Generate all frames
        print("Generating frames...")
        frame_paths = []
        for i in range(total_frames):
            if i % fps == 0:  # Progress update every second
                print(f"Processing second {i//fps} of {int(audio.duration_seconds)}")
            frame_paths.append(save_frame(i))

        # Create video from frames using Full HD resolution
        print("Creating video...")
        frame = cv2.imread(frame_paths[0])

        video = cv2.VideoWriter(
            output_video,
            cv2.VideoWriter_fourcc(*'mp4v'),
            fps,
            (hd_width, hd_height)
        )

        for frame_path in frame_paths:
            # Read frame and ensure it has the right dimensions
            frame = cv2.imread(frame_path)
            if frame.shape[:2] != (hd_height, hd_width):
                frame = cv2.resize(frame, (hd_width, hd_height))
            video.write(frame)

        video.release()
        plt.close()

    print("Done! Full HD video saved to:", output_video)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Create a video visualization of an mp3 file.')
    parser.add_argument('audio', type=str, help='The input audio.')
    parser.add_argument('--output', '-o', type=str, default='output.mp4', help='The output video.')
    argv = parser.parse_args()

    create_audio_visualization(
        input_audio=argv.audio,
        output_video=argv.output,
        fps=30
    )
