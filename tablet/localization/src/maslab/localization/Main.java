package maslab.localization;

import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

import javax.imageio.ImageIO;

/**
 * Main for the localization thread
 *  
 * @author akhil
 *
 */

public class Main {

	/**
	 * main for this stuff
	 * TODO: actually compute binary image from what's given
	 */
	public static void main(String[] args) {
		final int port = 2302;
		
		
		try {
			final BufferedImage image = ImageIO.read(new File("C:\\Users\\akhil\\Documents\\MASLAB\\shadercl\\ShaderCL\\ShaderCL Examples\\images\\map_dt.png"));
			Thread t = new Thread() {
				public void run() {
					Localizer localizer = new Localizer(image);
					final LocalizationServer localServer = new LocalizationServer(port, localizer);
					localServer.startServer();
				}
			};
			t.start();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
//		testCommunication();
	}
	
	private static void testCommunication() {
		try {
			System.out.println("got here");
			Socket cock = new Socket("localhost",2302);
			PrintWriter out = new PrintWriter(cock.getOutputStream(), true);
			BufferedReader in = new BufferedReader(
					new InputStreamReader(cock.getInputStream()));
			
			out.println("{\"measurements\":[\"0.654100135084239\",\"0.7140298455195194\",\"0.6556403936212141\",\"0.5585515641826985\"]}");
			System.out.println(in.readLine());
			out.println("exit");
			cock.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	
}
