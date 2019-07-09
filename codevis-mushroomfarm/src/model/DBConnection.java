package model;

import java.sql.Connection;
import java.sql.DriverManager;

import javax.swing.JOptionPane;

public class DBConnection {
	
	public Connection getConnection(){
		Connection myConn = null;
		try{
			String url = "jdbc:mysql://localhost:3306/mushroom_farm?useUnicode=true&characterEncoding=UTF-8";
			String user = "root";
			String pwd = "";
			myConn = DriverManager.getConnection(url, user, pwd);
		}catch(Exception e){
			JOptionPane.showMessageDialog(null, "Error connection");
		}
		return myConn;
	}
}
