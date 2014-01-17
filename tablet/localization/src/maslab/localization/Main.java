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
			final BufferedImage image = ImageIO.read(new File("C:\\Users\\akhil\\Documents\\MASLAB\\shadercl\\ShaderCL\\ShaderCL Examples\\images\\map_dt2.png"));
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
			
//			out.println("{\"measurements\":[\"0.7081397145966423\",\"0.7094861012963988\",\"0.7021630416732194\",\"0.7004442691083548\"]}"); // 0.5,0.5,45
//			System.out.println(in.readLine());
			out.println("{\"measurements\":[\"0.7196930784229848\",\"0.5821820280118326\",\"0.5769988321789806\",\"0.7957202438799321\"]}"); // 0.5,0.5,60
			System.out.println(in.readLine());
//			out.println("{\"measurements\":[\"0.8269265314931968\",\"0.57764893460754\",\"0.5625262498947508\",\"1.100190533600091\"]}"); // 0.5,0.5,75
//			System.out.println(in.readLine());
////			out.println("{\"measurements\":[\"0.4909850483700776\",\"0.5894288578031636\",\"0.5034472231493763\",\"1.498484935652294\"]}"); // 0.5,0.5,90
//			System.out.println(in.readLine());
			out.println("exit");
			cock.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	
}
