package maslab.localization;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;

/**
 * Takes care of the socket IO. Input = sensor measurements. Output = points
 * 
 * @author akhil
 *
 */

public class LocalizationServer {

	private ServerSocket svrSock;
	private Socket cliSock;
	private PrintWriter outputWriter;
	private BufferedReader inputReader;
	private Localizer localizer;
	
	public LocalizationServer(int port, Localizer localizer) {
		this.localizer = localizer;
		try {
			this.svrSock = new ServerSocket(port);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * starts actually reading the input from the connection
	 * and writing back the guesses of points. 
	 * 
	 * input = JSON. format: {"measurements":["<number>","<number>",...]}
	 * output = json. format: {"confidentPoints" : [["<x>","<y>","theta"],...]}
	 */
	public void startServer() {
		try {
			this.cliSock = svrSock.accept();
//			System.out.println("accepted connection");
			this.outputWriter = new PrintWriter(cliSock.getOutputStream(), true);
			this.inputReader = new BufferedReader(
					new InputStreamReader(cliSock.getInputStream()));
		} catch (IOException ioe) {
			ioe.printStackTrace();
		}
		String measurementsField = "measurements";
		String input, output;
		while(true) {
			try {
				input = inputReader.readLine(); //json
				if (input == null)
					continue;
				if (input.equals("exit")) {
					break;
				}
				Object obj = JSONValue.parse(input);
				JSONObject json = (JSONObject)obj;
				if (json == null)
					continue;
				JSONArray measurements = (JSONArray)(json.get(measurementsField));
				float[] distances = new float[measurements.size()]; //this is what we give to Localizer
				for (int i = 0; i < distances.length; i++) {
					distances[i] = Float.valueOf(measurements.get(i).toString());
				}
				
				//run the localizer and recieve points
				List<List<Float>> points = localizer.processSensorMeasurements(distances);
				//TODO: handle too many points to return
				
				//write most confident points back to client in json
				Map<String,List<List<Float>>> map = new HashMap<String,List<List<Float>>>();
				map.put("confidentPts", points);
				output = JSONValue.toJSONString(map);
//				System.out.println(output);
				outputWriter.println(output);
				
			} catch (IOException ioe) {
				ioe.printStackTrace(); //maybe find something better to do here.
			}
		}
		try {
			cliSock.close();
			svrSock.close();
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
