import numpy as np
import SimpleITK as sitk

class Metrics():
    def __init__(self, segmented_image, ground_truth_mask):
        """
        Initialize the Metrics class with segmented image and ground truth mask.

        Parameters:
        segmented_image (SimpleITK.Image): The segmented image.
        ground_truth_mask (SimpleITK.Image): The ground truth mask.
        """
        self.segmented_image = segmented_image
        self.ground_truth_mask = ground_truth_mask
        self.segmented_array = sitk.GetArrayFromImage(self.segmented_image)
        self.ground_truth_array = sitk.GetArrayFromImage(self.ground_truth_mask)

        self.tp = np.sum((self.segmented_array == 1) & (self.ground_truth_array == 1))
        self.fp = np.sum((self.segmented_array == 1) & (self.ground_truth_array == 0))
        self.fn = np.sum((self.segmented_array == 0) & (self.ground_truth_array == 1))
        self.tn = np.sum((self.segmented_array == 0) & (self.ground_truth_array == 0))

    def GetTruePositiveCount(self):
        """
        Get the count of true positives (TP).

        Returns:
        int: The number of true positives.
        """
        return self.tp

    def GetFalsePositiveCount(self):
        """
        Get the count of false positives (FP).

        Returns:
        int: The number of false positives.
        """
        return self.fp

    def GetTrueNegativeCount(self):
        """
        Get the count of true negatives (TN).

        Returns:
        int: The number of true negatives.
        """
        return self.tn

    def GetFalseNegativeCount(self):
        """
        Get the count of false negatives (FN).

        Returns:
        int: The number of false negatives.
        """
        return self.fn

    def GetSensitivity(self):
        """
        Get the sensitivity (also known as Recall).

        Sensitivity = TP / (TP + FN)

        Returns:
        float: The sensitivity.
        """
        sensitivity = self.tp / (self.tp + self.fn) if (self.tp + self.fn) != 0 else 0
        return sensitivity

    def GetSpecificity(self):
        """
        Get the specificity.

        Specificity = TN / (TN + FP)

        Returns:
        float: The specificity.
        """
        specificity  = self.tn / (self.tn + self.fp) if (self.tn + self.fp) != 0 else 0
        return specificity

    def GetPositivePredictiveValue(self):
        """
        Get the positive predictive value (PPV, also known as Precision).

        PPV = TP / (TP + FP)

        Returns:
        float: The positive predictive value.
        """
        ppv = self.tp / (self.tp + self.fp) if (self.tp + self.fp) != 0 else 0
        return ppv

    def GetNegativePredictiveValue(self):
        """
        Get the negative predictive value (NPV).

        NPV = TN / (TN + FN)

        Returns:
        float: The negative predictive value.
        """
        npv = self.tn / (self.tn + self.fn) if (self.tn + self.fn) != 0 else 0
        return npv

    def GetFalseNegativeRate(self):
        """
        Get the false negative rate (FNR, also known as Miss Rate).

        FNR = FN / (FN + TP)

        Returns:
        float: The false negative rate.
        """
        FNR = self.fn / (self.fn + self.tp) if (self.fn + self.tp) != 0 else 0
        return FNR

    def GetFalsePositiveRate(self):
        """
        Get the false positive rate (FPR, also known as Fall-out).

        FPR = FP / (FP + TN)

        Returns:
        float: The false positive rate.
        """
        FPR = self.fp / (self.fp + self.tn) if (self.fp + self.tn) != 0 else 0
        return FPR

    def GetDiceCoefficient(self):
        """
        Get the Dice coefficient (also known as F1 Score).

        Dice Coefficient = (2 * TP) / (2 * TP + FP + FN)

        Returns:
        float: The Dice coefficient.
        """
        return (2 * self.tp) / (2 * self.tp + self.fp + self.fn)

    def GetJaccardIndex(self):
        """
        Get the Jaccard index (also known as Intersection over Union).

        Jaccard Index = TP / (TP + FP + FN)

        Returns:
        float: The Jaccard index.
        """
        return self.tp / (self.tp + self.fp + self.fn)

    def GetAccuracy(self):
        """
        Get the accuracy.

        Accuracy = (TP + TN) / (TP + TN + FP + FN)

        Returns:
        float: The accuracy.
        """
        return (self.tp + self.tn) / (self.tp + self.tn + self.fp + self.fn)
