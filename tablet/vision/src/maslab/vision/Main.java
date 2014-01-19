package maslab.vision;


import java.awt.BorderLayout;
import java.awt.image.BufferedImage;
import java.awt.image.ImageObserver;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;
import java.util.Map;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfByte;
import org.opencv.core.Size;

import org.opencv.core.Mat;
import org.opencv.highgui.Highgui;
import org.opencv.highgui.VideoCapture;
import org.opencv.imgproc.Imgproc;

public class Main {

	public static final int DEFAULT_CAM = 1;
	public static final int DEFAULT_PORT = 2300;
	
	public static void main (String args[]) {
		// Load the OpenCV library
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);

		int camIdx, port;
		if (args.length == 0) {
			camIdx = DEFAULT_CAM;
			port = DEFAULT_PORT;
		} else if (args.length == 1) {
			camIdx = DEFAULT_CAM;
			port = Integer.parseInt(args[0]);
		} else {
			port = Integer.parseInt(args[0]);
			camIdx = Integer.parseInt(args[1]);
		}
		
		// Setup the camera
		VideoCapture camera = new VideoCapture();
		camera.open(camIdx);
		
		// Create GUI windows to display camera output and OpenCV output
		int width = (int) (camera.get(Highgui.CV_CAP_PROP_FRAME_WIDTH));
		int height = (int) (camera.get(Highgui.CV_CAP_PROP_FRAME_HEIGHT));
//		JLabel cameraPane = createWindow("Camera output", width, height);
//		JLabel opencvPane = createWindow("OpenCV output", width, height);

		// Set up structures for processing images
//		ImageProcessor processor = new ImageProcessor();
		Mat rawImage = new Mat();
		FrameProcessor fp = new FrameProcessor();
		VisionPublisher vp = new VisionPublisher(port);
//		Mat processedImage = new Mat();
//		Mat2Image rawImageConverter = new Mat2Image(BufferedImage.TYPE_3BYTE_BGR);
//		Mat2Image processedImageConverter = new Mat2Image(BufferedImage.TYPE_BYTE_GRAY);
		
		while (true) {
			// Wait until the camera has a new frame
			while (!camera.read(rawImage)) {
				try {
					Thread.sleep(1);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
			
			Map<String, List<double[]>> blobs = fp.processFrame(rawImage);
			List<List<Double>> reactors = ReactorFinder.findReactors(rawImage);
			Map<String, List<List<Double>>> balls = BlobProcessor.processBlobs(blobs);
			vp.publish(balls, reactors);
			
			// Update the GUI windows
//			updateWindow(cameraPane, rawImage, rawImageConverter);
//			updateWindow(opencvPane, processedImage, processedImageConverter);
			
			try {
				Thread.sleep(10);
			} catch (InterruptedException e) { }
		}
//		vp.close();
	}
	
//    private static JLabel createWindow(String name, int width, int height) {    
//        JFrame imageFrame = new JFrame(name);
//        imageFrame.setSize(width, height);
//        imageFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
//        
//        JLabel imagePane = new JLabel();
//        imagePane.setLayout(new BorderLayout());
//        imageFrame.setContentPane(imagePane);
//        
//        imageFrame.setVisible(true);
//        return imagePane;
//    }
//    
//    private static void updateWindow(JLabel imagePane, Mat mat, Mat2Image converter) {
//    	int w = (int) (mat.size().width);
//    	int h = (int) (mat.size().height);
//    	if (imagePane.getWidth() != w || imagePane.getHeight() != h) {
//    		imagePane.setSize(w, h);
//    	}
//    	BufferedImage bufferedImage = converter.getImage(mat);
//    	imagePane.setIcon(new ImageIcon(bufferedImage));
//    }

}