import cv2


def padder(image, patch_size):
    """
    Pad an input image so that its dimensions become divisible by a specified patch size.

    This function adds padding around the input image to ensure its height and width
    are multiples of the patch size. This is useful for processing images in patches
    during tasks like image segmentation using models that require inputs of specific sizes.

    :param image: Input image to be padded.
    :type image: numpy.ndarray, shape (H, W, C)
    :param patch_size: Size of the patches the image will be divided into.
    :type patch_size: int
    :return: Padded image with dimensions divisible by patch_size.
    :rtype: numpy.ndarray, shape (H_padded, W_padded, C)

    **Usage:**

    This function pads the input image so that its dimensions are divisible by the specified patch size.

    **Example:**

    .. code-block:: python

        import cv2
        from your_module import padder

        image = cv2.imread("input_image.png")
        patch_size = 256
        padded_image = padder(image, patch_size)
        cv2.imwrite("padded_image.png", padded_image)

    **Details:**

    - Computes the required padding to make the image dimensions divisible by the patch size.
    - Adds padding evenly around the image.
    - Returns the padded image with dimensions (H_padded, W_padded, C).

    **Dependencies:**

    This function requires the OpenCV library (`cv2`) for image manipulation.

    :note: Ensure the input image has channels in the order (height, width, channels) for correct padding.

    :author: Lea Bancovac
    """

    h = image.shape[0]
    w = image.shape[1]
    height_padding = ((h // patch_size) + 1) * patch_size - h
    width_padding = ((w // patch_size) + 1) * patch_size - w

    top_padding = int(height_padding / 2)
    bottom_padding = height_padding - top_padding

    left_padding = int(width_padding / 2)
    right_padding = width_padding - left_padding

    padded_image = cv2.copyMakeBorder(
        image,
        top_padding,
        bottom_padding,
        left_padding,
        right_padding,
        cv2.BORDER_CONSTANT,
        value=[0, 0, 0],
    )

    return padded_image
