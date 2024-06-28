import keras.backend as K


# Let's implement two custom metrics f1 score and iou
def f1(y_true, y_pred):
    """
    Compute the F1 score metric for binary classification.

    :param y_true: True labels.
    :type y_true: keras.tensor.Tensor
    :param y_pred: Predicted labels.
    :type y_pred: keras.tensor.Tensor
    :return: F1 score value.
    :rtype: keras.tensor.Tensor
    :author: Rens van den Berg

    **Usage:**

    This function calculates the F1 score for binary classification tasks.

    **Example:**

    .. code-block:: python

        import keras.backend as K
        from your_module import f1

        y_true = K.variable([[1, 0, 1], [0, 1, 0]])
        y_pred = K.variable([[1, 0, 0], [0, 1, 1]])

        f1_score = f1(y_true, y_pred)
        print(K.eval(f1_score))  # Output: 0.6666667

    **Details:**

    The function first defines two helper functions:
    
    - `recall_m`: Computes the recall metric.
    - `precision_m`: Computes the precision metric.

    The F1 score is then computed as the harmonic mean of precision and recall.

    The function returns the F1 score as a Keras tensor.
    """

    def recall_m(y_true, y_pred):
        TP = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        Positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = TP / (Positives + K.epsilon())
        return recall

    def precision_m(y_true, y_pred):
        TP = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        Pred_Positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = TP / (Pred_Positives + K.epsilon())
        return precision

    precision, recall = precision_m(y_true, y_pred), recall_m(y_true, y_pred)

    return 2 * ((precision * recall) / (precision + recall + K.epsilon()))


def iou(y_true, y_pred):
    """
    Compute the Intersection over Union (IoU) metric.

    :param y_true: True labels.
    :type y_true: keras.tensor.Tensor
    :param y_pred: Predicted labels.
    :type y_pred: keras.tensor.Tensor
    :return: IoU score value.
    :rtype: keras.tensor.Tensor
    :author: Rens van den Berg

    **Usage:**

    This function calculates the Intersection over Union (IoU) for evaluating the accuracy of an object detector on a particular dataset.

    **Example:**

    .. code-block:: python

        import keras.backend as K
        from your_module import iou

        y_true = K.variable([[[[1], [0]], [[1], [0]]]])
        y_pred = K.variable([[[[1], [0]], [[0], [1]]]])

        iou_score = iou(y_true, y_pred)
        print(K.eval(iou_score))  # Output: 0.33333334

    **Details:**

    The function defines a helper function `f` that calculates the IoU for each image in the batch. The IoU is computed as the ratio of the intersection area to the union area of the true and predicted labels.

    The function returns the mean IoU score across the batch as a Keras tensor.
    """

    def f(y_true, y_pred):
        intersection = K.sum(K.abs(y_true * y_pred), axis=[1, 2, 3])
        total = K.sum(K.square(y_true), [1, 2, 3]) + K.sum(K.square(y_pred), [1, 2, 3])
        union = total - intersection
        return (intersection + K.epsilon()) / (union + K.epsilon())

    return K.mean(f(y_true, y_pred), axis=-1)
