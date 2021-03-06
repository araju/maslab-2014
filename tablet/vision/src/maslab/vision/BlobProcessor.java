package maslab.vision;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


public class BlobProcessor {

	
	/**
	 * Processes list of blobs from the {@link FrameProcessor}. Filters out balls  that are too high/too far away
	 * 
	 * @param blobs - map of color to list of blob centers [x,y]
	 * @return map of ball color to list of direction and distances of each ball, 
	 * 		sorted by distance (closest first)
	 */
	public static Map<String, List<List<Double>>>processBlobs(Map<String,List<double[]>> blobs) {
		Map<String, List<List<Double>>> balls = new HashMap<String, List<List<Double>>>();
		
		for (String color : blobs.keySet()) {
			balls.put(color, new ArrayList<List<Double>>());
			for (double[] point : blobs.get(color)) {
				ArrayList<Double> b = new ArrayList<Double>();
				double direction, distance;
				if (color.equals("teal") || color.equals("yellow")) {
					direction = calculateReactorDirection(point[0],point[1]);
					distance = calculateReactorDistance(point[0],point[1]);
				} else if (color.equals("wallEnds")) {
					direction = point[0]; // not actually a direction or distance. just a place holder
					distance = point[1];
				} else {
					direction = calculateDirection(point[0]);
					distance = color.equals("blue") ? calculateWallDistance(point[0],point[1]) : calculateDistance(point[0],point[1]);
				}
				if (distance > 0) {
					b.add(direction);
					b.add(distance);
					if (color.equals("teal") || color.equals("yellow")) {
						b.add(point[2]);
						b.add(point[3]);
					}
					balls.get(color).add(b);
				}
			}
			if (color.equals("red") || color.equals("green") || color.equals("teal") || color.equals("yellow")) {
				Collections.sort(balls.get(color), new Comparator<List<Double>>() {
	
					@Override
					public int compare(List<Double> ball1, List<Double> ball2) {
						if (ball1.get(1) < ball2.get(1))
							return -1;
						else if (ball1.get(1) > ball2.get(1))
							return 1;
						else
							return 0;
					}
					
				});
			}
		}
		return balls;
	}
	
	//TODO: find out if other info is more useful for figuring out how far away the reactor is
	
	private static double calculateReactorDistance(double x, double y) {
//		double zDist = 1050.0 / (y - 255.0);
//		double xDist = zDist * x / 340.0;
//		double dist = Math.sqrt(Math.pow(xDist,2) + Math.pow(zDist,2));
//		return dist;
		return (240 - y);
	}


	private static double calculateReactorDirection(double x, double y) {
		return calculateDirection(x);
	}

	// screw it, just return the y
	public static double calculateDistance(double x, double y) {
//		double zDist;
//		if (y > 80.0)
//			zDist = 3500.0 / (y - 80.0);
//		else
//			return -1;  // TODO figure out a better solution for this stuff. right now, if too far, don't consider it a valid ball.
//		double xDist = zDist * x / 340.0;
//		double dist = Math.sqrt(Math.pow(xDist,2) + Math.pow(zDist,2));
//		return dist;
		if (y < 25.0) return -1.0;
		
		return (240 - y);
	}
	
	
	// for walls, we cannot use our ground assumption we used for calculate distance
	// for now just return the pure y coordinate.
	public static double calculateWallDistance(double x, double y) {
		return y;
	}


	public static double calculateDirection(double x) {
		x = x*2;
		return Math.toDegrees(Math.atan((x - 320.0) / 340.0));
	}



	/**
	 * main method just for testing
	 */
	public static void main(String[] args) {
		//
	}

}
