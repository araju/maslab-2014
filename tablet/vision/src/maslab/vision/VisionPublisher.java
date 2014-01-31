package maslab.vision;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.simple.JSONValue;

/**
 * This actually publishes the info in json format to some socket
 * 
 * @author akhil
 *
 */


public class VisionPublisher {

	private int port;
	private Socket socket;
//	private PrintWriter outputWriter;
	private BufferedWriter outputWriter;
	
	private final String HOST = "localhost";
	
	public VisionPublisher(int port) {
		this.port = port;
		while (this.socket == null) {
			try {
				this.socket = new Socket(HOST, this.port);
//				outputWriter = new PrintWriter(this.socket.getOutputStream(), true);
				outputWriter = new BufferedWriter(new OutputStreamWriter(this.socket.getOutputStream()));
			} catch (IOException ioe) {
				ioe.printStackTrace();
			}
		}
	}
	
	
	/**
	 * Publishes to socket in json format:
	 *  {
			<ball_color>:[[<direction>,<distance>],...]
			"reactor":[[<direction>,<distance>,<orientation>],...]
		}
	 * 
	 * @param balls
	 * @param reactors
	 */
	public void publish(Map<String,List<List<Double>>> balls, List<List<Double>> reactors) {
			Map<String, List<Double>> sendMap = new HashMap<String, List<Double>>();
			for (String color : balls.keySet()) {
				if (balls.get(color).size() > 0) {
					if (color.equals("teal")) {
						sendMap.put("reactors", balls.get(color).get(0));
					} else {
						sendMap.put(color, balls.get(color).get(0));
					}
				} else {
					if (color.equals("teal")) {
						sendMap.put("reactors", new ArrayList<Double>());
					} else {
						sendMap.put(color, new ArrayList<Double>());
					}
				}
			}
		
	//		if (reactors != null && reactors.size() > 0) {
	//			sendMap.put("reactors", reactors.get(0));
	//		} else {
	//			sendMap.put("reactors", new ArrayList<Double>());
	//		}
			
			String json = JSONValue.toJSONString(sendMap);
			System.out.println(json);
		try {
//			System.out.println("Before Write");
			outputWriter.write(json);
//			System.out.println("After write");
			outputWriter.newLine();
//			System.out.println("After newline");
			outputWriter.flush();
//			System.out.println("After flush");
		}
		catch (IOException ioe) {
			ioe.printStackTrace();
			try {
				this.socket = new Socket(this.HOST, this.port);
				this.outputWriter = new BufferedWriter(new OutputStreamWriter(this.socket.getOutputStream()));
			} catch (UnknownHostException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
	
	public void close() {
		try {
			outputWriter.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	
	
	
	/**
	 * main method just for testing
	 */
	public static void main(String[] args) {
		//
	}

}
