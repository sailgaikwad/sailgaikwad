import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import scipy.ndimage as ndi

def segment_subject(rgb_np):
    # Background in upper-right / right side:
    # Let's inspect the background colors.
    # In crop_test1, background is mainly in upper right (x > 150, y < 220) and far right.
    # Pillars are warm beige/grey, train bokeh is muted cyan/brown.
    # The subject is:
    # Hair: black/dark (low value)
    # Face: warm skin
    # Sweater: vivid red (high R, low G, low B: R - G > 40, R - B > 40)
    # Glasses: dark sunglasses
    
    # We can compute color distance to background or use a color model / seed.
    # Sample background patches: e.g. top right corner (x in [160, 290], y in [0, 150])
    bg_sample = rgb_np[0:150, 180:300].reshape(-1, 3).astype(np.float32)
    bg_mean = np.median(bg_sample, axis=0)
    
    # Or color distance from background cluster:
    diff = np.linalg.norm(rgb_np.astype(np.float32) - bg_mean, axis=2)
    
    # Also red sweatshirt is definitely subject:
    is_red = (rgb_np[:, :, 0] > 110) & (rgb_np[:, :, 1] < 70) & (rgb_np[:, :, 2] < 70)
    # Face skin:
    is_skin = (rgb_np[:, :, 0] > rgb_np[:, :, 1]) & (rgb_np[:, :, 1] > rgb_np[:, :, 2]) & (rgb_np[:, :, 0] > 100) & (rgb_np[:, :, 2] < 120) & (~is_red)
    # Dark hair / glasses / shadow:
    is_dark = (rgb_np[:, :, 0] < 65) & (rgb_np[:, :, 1] < 65) & (rgb_np[:, :, 2] < 65)
    
    # Initial foreground mask
    fg_init = (diff > 55) | is_red | (is_dark & (np.arange(340)[:, None] < 260) & (np.arange(300)[None, :] < 180))
    
    # Also anything on the left half that is subject body
    # Let's clean up with binary closing and fill holes
    struct = ndi.generate_binary_structure(2, 2)
    closed = ndi.binary_closing(fg_init, structure=struct, iterations=4)
    filled = ndi.binary_fill_holes(closed)
    
    # Keep largest connected component
    labeled, num_features = ndi.label(filled)
    if num_features > 0:
        sizes = ndi.sum(filled, labeled, range(1, num_features + 1))
        max_label = np.argmax(sizes) + 1
        mask = (labeled == max_label)
    else:
        mask = filled
        
    mask = ndi.binary_fill_holes(mask)
    return mask

def main():
    img = Image.open('crop_test1.png').convert('RGB')
    rgb_np = np.array(img)
    mask = segment_subject(rgb_np)
    
    # Save mask to visually check
    mask_img = Image.fromarray((mask * 255).astype(np.uint8))
    mask_img.save('mask_test.png')
    print('Saved mask_test.png')

if __name__ == '__main__':
    main()
