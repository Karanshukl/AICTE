import cv2
import os
import hashlib
import random
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def hash_password(password):
    """Hash the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def encrypt_message_in_image(img, msg):
    """Encrypt the message into the image."""
    n, m, z = 0, 0, 0
    for char in msg:
        img[n, m, z] = ord(char)
        n, m, z = get_next_pixel(n, m, z, img.shape)
    return img

def decrypt_message_from_image(img, msg_length):
    """Decrypt the message from the image."""
    message = ""
    n, m, z = 0, 0, 0
    for _ in range(msg_length):
        message += chr(img[n, m, z])
        n, m, z = get_next_pixel(n, m, z, img.shape)
    return message

def get_next_pixel(n, m, z, shape):
    """Get the next pixel coordinates in a randomized manner."""
    n += 1
    if n >= shape[0]:
        n = 0
        m += 1
    if m >= shape[1]:
        m = 0
        z = (z + 1) % 3
    return n, m, z

def encrypt_message():
    img_path = "E:/karan shukla/Edunet/mypic.jpg"
    img = cv2.imread(img_path)
    if img is None:
        logging.error("Error: Could not load image")
        return
    
    msg = input("Enter secret message: ")
    password = input("Enter a passcode: ")
    hashed_password = hash_password(password)
    
    # Check if message is too long for the image
    max_message_length = img.shape[0] * img.shape[1] * 3
    if len(msg) > max_message_length:
        logging.error(f"Error: Message too long for this image. Max length: {max_message_length}")
        return
    
    # Pad the message if necessary
    msg = msg.ljust(max_message_length, '\0')
    
    # Encrypt message
    img = encrypt_message_in_image(img, msg)
    
    # Save encrypted image
    try:
        encrypted_img_path = "encrypted_Image.jpg"
        cv2.imwrite(encrypted_img_path, img)
        logging.info(f"Encrypted image saved as {encrypted_img_path}")
        os.system(f"start {encrypted_img_path}")
    except Exception as e:
        logging.error(f"Error saving image: {e}")
        return
    
    # Decrypt message
    pas = input("Enter passcode for Decryption: ")
    if hash_password(pas) == hashed_password:
        decrypted_msg = decrypt_message_from_image(img, len(msg))
        logging.info(f"Decrypted message: {decrypted_msg.strip()}")
    else:
        logging.error("YOU ARE NOT authorized")

if __name__ == "__main__":
    encrypt_message()