package maslab.vision;

import java.awt.image.BufferedImage;
import java.util.ArrayList;
import java.util.List;

import org.opencv.core.Core;
import org.opencv.core.Mat;

import com.google.zxing.BinaryBitmap;
import com.google.zxing.LuminanceSource;
import com.google.zxing.RGBLuminanceSource;
import com.google.zxing.ReaderException;
import com.google.zxing.Result;
import com.google.zxing.ResultMetadataType;
import com.google.zxing.ResultPoint;
import com.google.zxing.common.HybridBinarizer;
import com.google.zxing.qrcode.QRCodeReader;

public class ReactorFinder {

	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}
	
	private static Mat2Image conv = new Mat2Image(BufferedImage.TYPE_3BYTE_BGR);
	private static QRCodeReader reader = new QRCodeReader();
	
	/**
	 * Returns list of reactors as triples (direction, distance, orientation)
	 * 
	 * @param frame
	 * @return
	 */
	public static List<List<Double>> findReactors(Mat frame) {
		BinaryBitmap bitmap = convertFrameToBitmap(frame);
		List<List<Double>> ret = new ArrayList<List<Double>>();
		try {
			Result result = reader.decode(bitmap);
			ResultPoint[] resPts = result.getResultPoints();
			if (resPts.length > 0) {
				List<Double> imgDims = getImageDimensions(resPts); //returns x,y,w,h
				//orientation explained: http://zxing.org/w/docs/javadoc/com/google/zxing/ResultMetadataType.html#ORIENTATION
				int orientation = ((Integer)(result.getResultMetadata().get(ResultMetadataType.ORIENTATION))).intValue();
				List<Double> physicalDims = getPhysicalDimensions(imgDims);
				physicalDims.add((double)orientation);
				ret.add(physicalDims);
			}
			return ret;
		} catch (ReaderException re) {
			return new ArrayList<List<Double>>();
		}
	}
	
	
	private static List<Double> getPhysicalDimensions(List<Double> imgDims) {
		// TODO Find calibration
		return null;
	}


	private static List<Double> getImageDimensions(ResultPoint[] resPts) {
		// find bounding box around pts, return the top left corner and the width, height
		double minX = -1;
		double maxX = -1;
		double minY = -1;
		double maxY = -1;
		for (ResultPoint pt : resPts) {
			double ptX = (double)pt.getX();
			double ptY = (double)pt.getY();
			if (minX == -1 || ptX < minX)
				minX = ptX;
			if (maxX == -1 || ptX > maxX)
				maxX = ptX;
			if (minY == -1 || ptY < minY)
				minY = ptY;
			if (maxY == -1 || ptY > maxY)
				maxY = ptY;
		}
		List<Double> ret = new ArrayList<Double>();
		ret.add(minX);
		ret.add(minY);
		ret.add(maxX - minX);
		ret.add(maxY - minY);
		return ret;
	}


	//TODO: test if this actually works. I'm a little skeptical
	private static BinaryBitmap convertFrameToBitmap(Mat frame) {		
		BufferedImage image = conv.getImage(frame);

		//convert the image to a binary bitmap source
		LuminanceSource source = new RGBLuminanceSource(image.getWidth(), image.getHeight(),
				image.getRGB(0, 0, image.getWidth(), image.getHeight(), null, 0, image.getWidth()));
		BinaryBitmap bitmap = new BinaryBitmap(new HybridBinarizer(source));
		return bitmap;
	}



	/**
	 * main method just for testing purposes
	 */
	public static void main(String[] args) {
		//
	}

}
