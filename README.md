# Clipping Algorithms
App word demonstration:

![image](https://github.com/AllerleiMal/ClippingAlgos/assets/76661587/3757a76f-ef8a-43a5-aa1f-f19530a97fb2)
![image](https://github.com/AllerleiMal/ClippingAlgos/assets/76661587/f21c15ed-0f53-4de5-9563-0dae8cfe467f)

A graphical application that uses matplotlib and tkinter to demonstrate the work of the implemented cutoff algorithms:
 - Liang Barskiy for segments;
   To apply the algorithm you need to create a txt file with the next structure:
   ```
   number of segments
   pairs of (x, y) coordinates of the beggining and the end of the semgents
   left-bottom and right-top (x, y) coordinates of the of the cutting off rectangle
   ```
 - Cyrus Beck for segments by polygon:
   ```
   number of segments
   pairs of (x, y) coordinates of the beggining and the end of the semgents
   number of clipping polygon vertexes
   pairs of (x, y) coordinates of the vertexes
   ```

# Packages
```
pip install matplotlib
pip install numpy
```
