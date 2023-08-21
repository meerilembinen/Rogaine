import cv2
import numpy as np

# Load an image
image = cv2.imread('../resources/thin_red_circle.png', cv2.IMREAD_GRAYSCALE)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(image, (9, 9), 2)

# Apply Hough Circle Transform
circles = cv2.HoughCircles(
    image,
    cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=100, param2=30, minRadius=10, maxRadius=1000
)
print(circles)

# Convert circles to integers
circles = np.uint16(np.around(circles))

# Draw circles on the original image
if circles is not None:
    circles = np.uint16(np.around(circles))

    # Filter out duplicate or closely spaced circles
    filtered_circles = []

    for circle in circles[0, :]:
        is_duplicate = False

        for existing_circle in filtered_circles:
            distance = np.sqrt((circle[0] - existing_circle[0]) ** 2 + (circle[1] - existing_circle[1]) ** 2)
            if distance < existing_circle[2] + circle[2]:
                is_duplicate = True
                break

        if not is_duplicate:
            filtered_circles.append(circle)

    # Draw circles on the original image
    for circle in filtered_circles:
        center = (circle[0], circle[1])
        radius = circle[2]
        cv2.circle(image, center, radius, (0, 255, 0), 2)

    # Display the image with detected circles
    cv2.imshow('Filtered Circles Detected', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No circles detected.")
