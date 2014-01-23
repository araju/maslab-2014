package maslab.vision;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
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
	private PrintWriter outputWriter;
	
	private final String HOST = "localhost";
	
	public VisionPublisher(int port) {
		this.port = port;
		while (this.socket == null) {
			try {
				this.socket = new Socket(HOST, this.port);
				outputWriter = new PrintWriter(this.socket.getOutputStream(), true);
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
				sendMap.put(color, balls.get(color).get(0));
			} else {
				sendMap.put(color, new ArrayList<Double>());
			}
		}
		
		if (reactors != null && reactors.size() > 0) {
			sendMap.put("reactors", reactors.get(0));
		} else {
			sendMap.put("reactors", new ArrayList<Double>());
		}
		
		String json = JSONValue.toJSONString(sendMap);
		outputWriter.println(json);
	}
	
	public void close() {
		outputWriter.close();
	}
	
	
	
	
	/**
	 * main method just for testing
	 */
	public static void main(String[] args) {
		//
	}

}
