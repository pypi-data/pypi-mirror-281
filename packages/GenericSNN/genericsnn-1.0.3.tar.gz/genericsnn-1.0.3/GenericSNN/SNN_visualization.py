import cv2
import matplotlib.pyplot as plt
import matplotlib
import os
from tensorflow import nn


def plot_input_video(images, imshape, output_path, filename):
    matplotlib.use('Agg')  # turn off gui
    for img in range(images.shape[0]):
        images_names = []
        for t in range(images.shape[1]):
            _, ax = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))
            ax.imshow(images[img, t, :].reshape(imshape))
            ax.set_title('Image ' + str(img) + ': ' + str(t))
            act_img_name = str(output_path / (filename + str(img) + str(t) + '.png'))
            images_names.append(act_img_name)
            plt.savefig(act_img_name)
        images_to_video(images_names, videoname=output_path / (filename + '_' + str(img)), remove_images=True)
    # matplotlib.use('QT4Agg')  # turn on gui


def plot_results_video(test_images, y_pred, imshape, output_path, filename):
    matplotlib.use('Agg')  # turn off gui
    n_clases = y_pred.shape[2]
    step = y_pred.shape[1]
    n_frames = test_images.shape[0] * step
    images_names = []

    for t in range(n_frames):
        act_img = int(t / step)
        act_pred = y_pred[act_img]
        act_t = t - step * act_img

        _, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
        axs[0].imshow(test_images[act_img, act_t, :].reshape(imshape))
        axs[1].bar(range(n_clases), nn.softmax(act_pred[act_t, :]))
        axs[1].grid()
        axs[1].set_ylim(0, 1)
        axs[1].set_title(str(act_t))
        act_img_name = str(output_path / (filename + str(t) + '.png'))
        images_names.append(act_img_name)
        plt.savefig(act_img_name)
    images_to_video(images_names, videoname=output_path / filename, remove_images=True)
    # matplotlib.use('QT4Agg')  # turn on gui


def images_to_video(images_names, videoname, remove_images=True, fps=30):
    # Save all images in a video

    print(images_names[0])
    height, width, _ = cv2.imread(images_names[0]).shape
    video = cv2.VideoWriter(str(videoname) + '.avi', 0, fps, (width, height))
    # Appending the images to the video one by one
    for image_name in images_names:
        video.write(cv2.imread(image_name))
    # Deallocating memories taken for window creation
    cv2.destroyAllWindows()
    video.release()  # releasing the video generated

    if remove_images:  # Remove images
        for image_names in images_names:
            os.remove(image_names)
