package maslab.vision;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.InputStream;
import java.io.OutputStream;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.IOUtils;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;

public class Mat2Image {
    BufferedImage img;
    byte[] dat;
    Mat convMat;
    int bufferedImageType;
    
    static {
//        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
    	loadLibrary();
    }
    
    public Mat2Image(int bufferedImageType) {
    	this.bufferedImageType = bufferedImageType;
    }

    public BufferedImage getImage(Mat mat) {
        allocateTempSpace(mat);
        if (mat.type() == CvType.CV_8UC3) {
        	Imgproc.cvtColor(mat, mat, Imgproc.COLOR_BGR2RGB);
        }
        mat.get(0, 0, dat);
    	img.getRaster().setDataElements(0, 0, img.getWidth(), img.getHeight(), dat);
        return img;
    }
    
    private void allocateTempSpace(Mat mat) {
        int w = mat.cols();
        int h = mat.rows();
        int c = mat.channels();
//        System.out.println(w);
//        System.out.println(h);
//        System.out.println(c);
        if (dat == null || dat.length != w * h * c) {
            dat = new byte[w * h * c];
//            System.out.println(1);
        }
        if (img == null || img.getWidth() != w || img.getHeight() != h) {
        	img = new BufferedImage(w, h, bufferedImageType);
//        	System.out.println(2);
        }
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
	                in = Mat2Image.class.getResourceAsStream("/opencv/x86/opencv_java248.dll");
	                fileOut = File.createTempFile("lib", ".dll");
	            }
	            else if (bitness == 64){
	                System.out.println("64 bit detected");
	                in = Mat2Image.class.getResourceAsStream("/opencv/x64/opencv_java248.dll");
	                fileOut = File.createTempFile("lib", ".dll");
	            }
	            else{
	                System.out.println("Unknown bit detected - trying with 32 bit");
	                in = Mat2Image.class.getResourceAsStream("/opencv/x86/opencv_java248.dll");
	                fileOut = File.createTempFile("lib", ".dll");
	            }
	        }
	        else if(osName.equals("Mac OS X")){
	            in = Mat2Image.class.getResourceAsStream("/opencv/mac/libopencv_java248.dylib");
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