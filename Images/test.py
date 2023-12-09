from PIL import Image, ImageSequence


def images_from_gif(filepath: str) -> list:
    background_image = Image.open(filepath)
    list = [frame.save(f'frame{i}.png') for i, frame in enumerate(ImageSequence.Iterator(background_image))]
    return list


images_from_gif("path.gif")