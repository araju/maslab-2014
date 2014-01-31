package maslab.vision;


import java.awt.BorderLayout;
import java.awt.image.BufferedImage;
import java.awt.image.ImageObserver;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.IOUtils;
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
	
	private static boolean run = true;
	
	public static void main (String args[]) {
		System.out.println("start main");
		
		// Load the OpenCV library
//		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
		loadLibrary();

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
		JLabel cameraPane = createWindow("Camera output", width, height);
//		JLabel opencvPane = createWindow("OpenCV output", width, height);

		// Set up structures for processing images
		Mat rawImage = new Mat();
		FrameProcessor fp = new FrameProcessor();
		VisionPublisher vp = new VisionPublisher(port);
		Mat processedImage = new Mat();
		Mat2Image rawImageConverter = new Mat2Image(BufferedImage.TYPE_3BYTE_BGR);
		Mat2Image processedImageConverter = new Mat2Image(BufferedImage.TYPE_BYTE_BINARY);
		try {
			while (true) {
				// Wait until the camera has a new frame
				long start = System.currentTimeMillis();
				while (!camera.read(rawImage)) {
	//				if (!cameraPane.isShowing() || !opencvPane.isShowing()) {
	//					break;
	//				}
					try {
						Thread.sleep(1);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
				}
				updateWindow(cameraPane, rawImage, rawImageConverter);
	//			processedImage = fp.testThresh(rawImage);
				Map<String, List<double[]>> blobs = fp.processFrame(rawImage, processedImage);
				List<List<Double>> reactors = null; //ReactorFinder.findReactors(rawImage);
				Map<String, List<List<Double>>> balls = BlobProcessor.processBlobs(blobs);
//				Map<String,List<List<Double>>> balls = new HashMap<String, List<List<Double>>>();
//				balls.put("green", new ArrayList<List<Double>>());
//				balls.put("red", new ArrayList<List<Double>>());
//				balls.put("reactors", new ArrayList<List<Double>>());
//				balls.put("wallEnds", new ArrayList<List<Double>>());
//				balls.put("yellow", new ArrayList<List<Double>>());
//				List<List<Double>> reactors = null;
				vp.publish(balls, reactors); //right now ignores the reactors list
				// Update the GUI windows
				
//				if (processedImage.width() > 0)
//					updateWindow(opencvPane, processedImage, processedImageConverter);
				
				try {
					Thread.sleep(10);
				} catch (InterruptedException e) {e.printStackTrace(); }
	//			if (!cameraPane.isShowing() || !opencvPane.isShowing()) {
	//				break;
	//			}
				System.out.println("Time: " + (System.currentTimeMillis() - start));
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		finally {
			vp.close();
			camera.release();
			System.out.println("Camera released");
		}
	}
	
    private static JLabel createWindow(String name, int width, int height) {    
        JFrame imageFrame = new JFrame(name);
        imageFrame.setSize(width, height);
        imageFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        JLabel imagePane = new JLabel();
        imagePane.setLayout(new BorderLayout());
        imageFrame.setContentPane(imagePane);
        
        imageFrame.setVisible(true);
        return imagePane;
    }
    
    private static void updateWindow(JLabel imagePane, Mat mat, Mat2Image converter) {
    	int w = (int) (mat.size().width);
    	int h = (int) (mat.size().height);
    	if (imagePane.getWidth() != w || imagePane.getHeight() != h) {
    		imagePane.setSize(w, h);
    	}
    	BufferedImage bufferedImage = converter.getImage(mat);
    	imagePane.setIcon(new ImageIcon(bufferedImage));
    }
    
    private static void loadLibrary() {
	    try {
	        InputStream in = null;
	        File fileOut = null;
	        String osName = System.getProperty("os.name");
	        System.out.println(osName);
	        if(osName.startsWith("Windows")){
	            int bitness = Integer.parseInt(System.getProperty("sun.arch.data.model"));
	            if(bitness == 32){
	                System.out.println("32 bit detected");
	                in = Main.class.getResourceAsStream("/opencv/x86/opencv_java248.dll");
	                fileOut = File.createTempFile("lib", ".dll");
	            }
	            else if (bitness == 64){
	                System.out.println("64 bit detected");
	                in = Main.class.getResourceAsStream("/opencv/x64/opencv_java248.dll");
	                fileOut = File.createTempFile("lib", ".dll");
	            }
	            else{
	                System.out.println("Unknown bit detected - trying with 32 bit");
	                in = Main.class.getResourceAsStream("/opencv/x86/opencv_java248.dll");
	                fileOut = File.createTempFile("lib", ".dll");
	            }
	        }
	        else if(osName.equals("Mac OS X")){
	            in = Main.class.getResourceAsStream("/opencv/mac/libopencv_java248.dylib");
	            fileOut = File.createTempFile("lib", ".dylib");
	        }


	        OutputStream out = FileUtils.openOutputStream(fileOut);
	        if (out == null) System.out.println("out is null");
	        if (in == null) System.out.println("in is null");
	        IOUtils.copy(in, out);
	        in.close();
	        out.close();
	        System.load(fileOut.toString());
	    } catch (Exception e) {
	        throw new RuntimeException("Failed to load opencv native library", e);
	    }
	}

}