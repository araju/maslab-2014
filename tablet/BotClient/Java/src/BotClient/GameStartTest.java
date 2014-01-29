package BotClient;

public class GameStartTest {
	public static void main( String[] args ) {
		
		BotClient botclient = new BotClient("18.150.7.174:6667","H4Lx8c0mOw",false); //our token: H4Lx8c0mOw, shared token: 1221
		
		while( !botclient.gameStarted() ) {
		}
		System.out.println("GAME-STARTED-BITCHES");
//		System.out.println("MAP --> " + botclient.getMap());
		try {
			Thread.sleep(180000); //3 minutes
		} catch (InterruptedException e) {
//			e.printStackTrace();
		} 
		botclient.close();
	}
}
