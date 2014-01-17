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
		
		testCommunication();
	}
	
	private static void testCommunication() {
		try {
			System.out.println("got here");
			Socket cock = new Socket("localhost",2302);
			PrintWriter out = new PrintWriter(cock.getOutputStream(), true);
			BufferedReader in = new BufferedReader(
					new InputStreamReader(cock.getInputStream()));
			
			out.println("{\"measurements\":[\"0.654100135084239\",\"0.7140298455195194\",\"0.6556403936212141\",\"0.5585515641826985\"]}"); // 0.5,0.5,45
			System.out.println(in.readLine());
			out.println("{\"measurements\":[\"0.7050573081244242\",\"0.44009522252057026\",\"0.4868010409981124\",\"0.8857089060876848\"]}"); // 0.5,0.5,60
			System.out.println(in.readLine());
			out.println("{\"measurements\":[\"0.8269265314931968\",\"0.57764893460754\",\"0.5625262498947508\",\"1.100190533600091\"]}"); // 0.5,0.5,75
			System.out.println(in.readLine());
//			out.println("{\"measurements\":[\"0.4909850483700776\",\"0.5894288578031636\",\"0.5034472231493763\",\"1.498484935652294\"]}"); // 0.5,0.5,90
//			System.out.println(in.readLine());
			out.println("exit");
			cock.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	
}
