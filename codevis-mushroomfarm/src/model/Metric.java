//package model;
//
//import java.sql.Connection;
//import java.sql.ResultSet;
//import java.sql.SQLException;
//import java.sql.Statement;
//
//public class Metric {
//	static Statement myStmt;
//	static ResultSet myRs;
//	public Metric(){
//		
//	}
//	public static void main(String [] args) throws SQLException{
//		int packageId = 0, referenceId = 0;
//		try{
//			DBConnection dbConn = new DBConnection();
//			Connection myConn = dbConn.getConnection();
//			myStmt = myConn.createStatement();
//		}catch(Exception e){
//			   e.printStackTrace();
//		}
//		//ambil projectPath dan projectName
//		myRs = myStmt.executeQuery("Select * from project");
//		if (myRs.next()){
//			String projectPath = myRs.getString(1);
//			System.out.println(projectPath);
//			String projectName = myRs.getString(2);
//			System.out.println(projectName);
//		}
//
//		//ambil mainClass
//		myRs = myStmt.executeQuery("Select * from method where name = 'main'");
//		if (myRs.next()){
//			referenceId = myRs.getInt(2);
//		}
//		myRs = myStmt.executeQuery("Select * from reference where referenceId = '"+referenceId+"'");
//		if (myRs.next()){
//			String mainClass = myRs.getString(3);
//			System.out.println(mainClass);
//			packageId = myRs.getInt(2);
//		}
//				
//		//ambil mainPackage
//		myRs = myStmt.executeQuery("Select * from package where packageId = '"+packageId+"'");
//		if (myRs.next()){
//			String mainPackage = myRs.getString(2);
//			System.out.println(mainPackage);
//		}		
//	}
//}
