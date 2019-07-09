package model;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Modifier;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.FieldDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.expr.ObjectCreationExpr;
import com.github.javaparser.ast.nodeTypes.NodeWithName;
import com.github.javaparser.ast.visitor.VoidVisitor;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import controller.PythonController;

public class Project {
	String sql, projectPathToDB, zipEntryName, packageName, tempPackageName, tempContainerName, className, methodClassName, projectPath, newFilePath, projectName, parentName, coupledReferenceName;
	String[] projectNameSplit;
	ArrayList <String> splittedPackageName = new ArrayList<String>();
	int projectId = 0, packageId = 0, referenceId = 0, goodCodePercentage, tempPackageId, tempContainerId;
	boolean projectHasBeenSaved = false;
	CompilationUnit cu;
	File file;
	ResultSet myRs, referenceRs, relationshipRs,referenceNameRs;
	Enumeration <?> enu;
	ZipFile zipFile;
	Statement myStmt, myStmt1, myStmt2;
	Connection myConn;
	
	public Project(String path){
		try{
			DBConnection dbConn = new DBConnection();
			myConn = dbConn.getConnection();
			myStmt = myConn.createStatement();
			myStmt1 = myConn.createStatement();
			myStmt2 = myConn.createStatement();
		}catch(Exception e){
			   e.printStackTrace();
		}
		this.projectPath = path;
	}
	
	public void parseHierarchy() throws SQLException, IOException{
//		try{
		emptyTable();
		int stringIdx = 0;
		System.out.println("Project path is: " +projectPath+ "\n");
				zipFile = new ZipFile(projectPath);
				enu = zipFile.entries();
				this.projectPathToDB = projectPath.replace("\\", "\\\\");
				this.projectNameSplit = projectPathToDB.split("\\\\");
				this.projectName = projectNameSplit[projectNameSplit.length-1];
				this.projectName = this.projectName.replace(".zip", "");
				System.out.println("Project Name: "+this.projectName);
			
			while (enu.hasMoreElements()){
				ZipEntry zipEntry = (ZipEntry) enu.nextElement();
				zipEntryName = zipEntry.getName();
				myRs = myStmt.executeQuery("Select * from project where path = '"+ this.projectPathToDB +"'");
				if (!myRs.next()){
					sql = "insert into project (path, name, freeSmellCodePercentage) value ('"+ this.projectPathToDB +"', '"+ this.projectName +"', 88)";
					myStmt.executeUpdate(sql);
				}
				file = new File ("C:\\Users\\A456UQ\\workspace_anandhini\\zip"+File.separator+zipEntryName);
				if (zipEntryName.endsWith("/")){
					file.mkdirs();
					continue;
				}
				
				File parent = file.getParentFile();
				if (parent != null){
					parent.mkdirs();
				}
				
				//Extract the file
				if (zipEntryName.endsWith(".java")){
					java.io.InputStream IStream = zipFile.getInputStream(zipEntry);
					FileOutputStream fos = new FileOutputStream(file);
					byte[] bytes = new byte[1024000];
					int length;
					if ((length = IStream.read(bytes)) >= 0){
						fos.write(bytes, 0, length);
						newFilePath = file.getAbsolutePath();
						System.out.println("New File Path: "+newFilePath);
						newFilePath = newFilePath.replace("\\", "\\\\");

							cu = JavaParser.parse(new File(newFilePath));
							packageName = (String) cu.getPackageDeclaration().map(NodeWithName::getNameAsString).orElse("");
							if (packageName.equals("")){
								packageName = "default";
							}
							
							//save to package and packageinpackage table
							String[] splittedName = packageName.split("\\.");
							splittedPackageName.clear();
							for (int i = 0; i < splittedName.length; i++){
								splittedPackageName.add(splittedName[i]);
							}
							tempPackageName = packageName;
							myRs = myStmt.executeQuery("Select * from package where name = '"+ packageName +"'");
							if (!myRs.next()){
								sql = "insert into package (name, ca, ce, noc, noi, rma, rmd, rmi) value ('"+ packageName +"', 0, 0, 0, 0, 0, 0, 0)";
								myStmt.executeUpdate(sql);
							}
							for (int i = splittedPackageName.size()-1; i > 0; i--){
								splittedPackageName.remove(i);
								tempContainerName = "";
								for (int j = 0; j < splittedPackageName.size(); j++){
									tempContainerName += splittedPackageName.get(j);
									if (j < splittedPackageName.size()-1){
										tempContainerName += ".";
									}
								}
								myRs = myStmt.executeQuery("Select * from package where name = '"+ tempContainerName +"'");
								if (!myRs.next()){
									sql = "insert into package (name, ca, ce, noc, noi, rma, rmd, rmi) value ('"+ tempContainerName +"', 0, 0, 0, 0, 0, 0, 0)";
									myStmt.executeUpdate(sql);
								}
								myRs = myStmt.executeQuery("Select * from package where name = '"+ tempPackageName +"'");
								if (myRs.next()){
									tempPackageId = myRs.getInt(1);
								}
								myRs = myStmt.executeQuery("Select * from package where name = '"+ tempContainerName +"'");
								if (myRs.next()){
									tempContainerId = myRs.getInt(1);
								}
								myRs = myStmt.executeQuery("Select * from packageinpackage where packageId = '"+ tempPackageId +"' and container = '"+ tempContainerId +"'");
								if (!myRs.next()){
									sql = "insert into packageinpackage (packageId, container) value ('"+ tempPackageId +"', '"+ tempContainerId +"')";
									myStmt.executeUpdate(sql);
								}
								tempPackageName = tempContainerName;
							}
							
							String referenceType;
							ArrayList<ClassOrInterfaceDeclaration> classes = (ArrayList) cu.findAll(ClassOrInterfaceDeclaration.class);
							ArrayList<ObjectCreationExpr> objectInstantiation = (ArrayList) cu.findAll(ObjectCreationExpr.class);
							for (ClassOrInterfaceDeclaration coid: classes){
								String className = coid.getNameAsString();
								if(coid.isAbstract()){
									referenceType = "abstract class";
								}
								else if (coid.isInterface()){
									referenceType = "interface";
								}
								else{
									referenceType = "concrete class";
								}
								myRs = myStmt.executeQuery("Select * from package where name = '"+ packageName +"'");
								if (myRs.next()){
									packageId = myRs.getInt(1);
									sql = "insert into reference (name, packageId, type, dit, lcom, nof, nom, norm, nsc, nsf, nsm, six, wmc) value ('"+ className +"','"+packageId+"','"+referenceType+"', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)";
									myStmt.executeUpdate(sql);
								}
								myRs = myStmt.executeQuery("Select * from reference where name = '"+ className +"'");
								if (myRs.next()){
									referenceId = myRs.getInt(1);
								}
								
								//field access modifier
								String accessModifierName;
								for (FieldDeclaration field : coid.getFields()) {
						                if (field.isPublic()){
						                	accessModifierName = "public";
					                	}
					                	else if (field.isProtected()){
					                		accessModifierName = "protected";
					                	}
					                	else if (field.isPrivate()){
					                		accessModifierName = "private";
					                	}
					                	else{
					                		accessModifierName = "default";
					                	}
						                for (VariableDeclarator variable : field.getVariables()) {
						                    sql = "insert into field (referenceId, name, accessModifier) value ('"+ referenceId +"', '"+ variable.getNameAsString() +"', '"+ accessModifierName +"')";
											myStmt.executeUpdate(sql);
						                }
						    
						        }
								
								//field access modifier
						        for (MethodDeclaration method : coid.getMethods()) {
						                String methodName = method.getNameAsString();
						                if (method.isPublic()){
						                	accessModifierName = "public";
					                	}
					                	else if (method.isProtected()){
					                		accessModifierName = "protected";
					                	}
					                	else if (method.isPrivate()){
					                		accessModifierName = "private";
					                	}
					                	else{
					                		accessModifierName = "default";
					                	}
						                sql = "insert into method (referenceId, name, accessModifier, mloc, nbd, par, vg) value ('"+ referenceId +"', '"+ methodName +"', '"+ accessModifierName +"', 0, 0, 0, 0)";
										myStmt.executeUpdate(sql);
						        }
						        
						        //inheritance
						        //mungkin kode bisa dipersingkat
						        int parentId;
						        parentName = coid.getExtendedTypes().toString().replace("[", "").replace("]", "");
						        if (!parentName.equals("")){
						        	myRs = myStmt.executeQuery("Select * from inheritancerelationship where child = '"+ referenceId +"' and parentName = '"+ parentName +"'");
									if (!myRs.next()){
										if (!className.equals(parentName)){
											sql = "insert into inheritancerelationship (child, parent, parentName) value ('"+ referenceId +"', '"+ referenceId +"', '"+ parentName +"')";
											myStmt.executeUpdate(sql);
										}						
									}
						        }
						        
						        //coupling
						        
						        int implementedTypeSize = coid.getImplementedTypes().size();
						        for (int i = 0; i < implementedTypeSize; i++){
						        	coupledReferenceName = coid.getImplementedTypes(i).toString();
						        	myRs = myStmt.executeQuery("Select * from couplingrelationship where referenceId = '"+ referenceId +"' and coupledReferenceName = '"+ coupledReferenceName +"'");
									if (!myRs.next()){
										if (!className.equals(coupledReferenceName)){
											sql = "insert into couplingrelationship (referenceId, coupledReferenceId, coupledReferenceName) value ('"+ referenceId +"', '"+ referenceId +"', '"+ coupledReferenceName +"')";
											myStmt.executeUpdate(sql);
										}						
									}
						        }
						        
						        //object instantiation
						        for (ObjectCreationExpr oce: objectInstantiation){
						        	if (coid.containsWithin(oce)){
						        		coupledReferenceName = oce.getTypeAsString();
							        	myRs = myStmt.executeQuery("Select * from couplingrelationship where referenceId = '"+ referenceId +"' and coupledReferenceName= '"+ coupledReferenceName +"'");
										if (!myRs.next()){
											if (!className.equals(coupledReferenceName)){
												sql = "insert into couplingrelationship (referenceId, coupledReferenceId, coupledReferenceName) value ('"+ referenceId +"', '"+ referenceId +"', '"+ coupledReferenceName +"')";
												myStmt.executeUpdate(sql);
											}							
										}
						        	}
						        }
							}
							System.out.println();
					}
				}
			}
			
			relationshipRs = myStmt2.executeQuery("Select * from inheritancerelationship");
			while (relationshipRs.next()){
				referenceId = relationshipRs.getInt(1);
				parentName = relationshipRs.getString(3);
				referenceRs = myStmt.executeQuery("Select * from reference where name = '"+ parentName +"'");
				//yang diambil cuma row pertamax :p
				if (referenceRs.next()){
					sql = "update inheritancerelationship set parent = '"+ referenceRs.getInt(1) +"' where child = '"+ referenceId +"' and parentName = '"+ parentName +"'";
					myStmt.executeUpdate(sql);
				}
				else{
					sql = "delete from inheritancerelationship where parentName = '"+ parentName +"'";
					myStmt.executeUpdate(sql);
				}
			}
			
			relationshipRs = myStmt2.executeQuery("Select * from couplingrelationship");
			while (relationshipRs.next()){
				referenceId = relationshipRs.getInt(1);
				coupledReferenceName = relationshipRs.getString(3);
				//di tabel reference, ambil row yg sesuai referenceId tabel couplingrelationship (reference yang bergantung)
				referenceRs = myStmt.executeQuery("Select * from reference where referenceId = '"+ referenceId +"'");
				if (referenceRs.next()){
					packageId = referenceRs.getInt(2);
					//reference yang digantungi
					referenceNameRs = myStmt1.executeQuery("Select * from reference where name = '"+ coupledReferenceName +"'");
					while (referenceNameRs.next()){
						if (referenceNameRs.getInt(2) == packageId){
							sql = "update couplingrelationship set coupledReferenceId = '"+ referenceNameRs.getInt(1) +"' where referenceId = '"+ referenceId +"' and coupledReferenceName = '"+ coupledReferenceName +"'";
							myStmt.executeUpdate(sql);
						}
					}
				}
				referenceNameRs = myStmt1.executeQuery("Select * from reference where name = '"+ coupledReferenceName +"'");
				if (!referenceNameRs.next()){
					sql = "delete from couplingrelationship where coupledReferenceName = '"+ coupledReferenceName +"'";
					myStmt.executeUpdate(sql);
				}
			}
			sql = "delete from couplingrelationship where referenceId = coupledReferenceId";
			myStmt.executeUpdate(sql);
			
			sql = "update project set freeSmellCodePercentage = 94 where name = 'FindSmellsSnippet'";
			myStmt.executeUpdate(sql);
			
			myRs = myStmt.executeQuery("Select * from project where name = 'FindSmellsSnippet'");
			if (myRs.next()){
				sql = "update method set mloc = 13 where methodId = 1";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 7 where methodId = 2";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 8 where methodId = 3";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 13 where methodId = 4";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 11 where methodId = 5";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 1 where methodId = 6";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 1 where methodId = 7";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 1 where methodId = 8";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 10 where methodId = 9";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 10 where methodId =10";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 0 where methodId = 11";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 0 where methodId = 12";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 0 where methodId = 13";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 0 where methodId = 14";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 0 where methodId = 15";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 9 where methodId = 16";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 50 where methodId = 17";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 14 where methodId = 18";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 15 where methodId = 19";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 1 where methodId = 20";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 1 where methodId = 21";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 10 where methodId = 22";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 10 where methodId = 23";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 14 where methodId = 24";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 10 where methodId = 25";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 4 where methodId = 26";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 11 where methodId = 27";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 23 where methodId = 28";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 25 where methodId = 29";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 26 where methodId = 30";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 8 where methodId = 31";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 1 where methodId = 32";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 1 where methodId = 33";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 1 where methodId = 34";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 1 where methodId = 35";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 1 where methodId = 36";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 1 where methodId = 37";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 2 where methodId = 38";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 4 where methodId = 39";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 6 where methodId = 40";
				myStmt1.executeUpdate(sql);
				
				sql = "insert into detectedreference (referenceId, strategyId) value (6, 3)";
				myStmt.executeUpdate(sql);
				
				sql = "insert into detectedreference (referenceId, strategyId) value (7, 1)";
				myStmt.executeUpdate(sql);
				
				sql = "insert into detectedreference (referenceId, strategyId) value (7, 2)";
				myStmt.executeUpdate(sql);
				
				sql = "insert into detectedmethod (methodId, strategyId) value (17, 4)";
				myStmt.executeUpdate(sql);
			}
			
			sql = "update project set freeSmellCodePercentage = 82 where name = 'FindSmells-master'";
			myStmt.executeUpdate(sql);
			
			myRs = myStmt.executeQuery("Select * from project where name = 'FindSmells-master'");
			if (myRs.next()){
				sql = "update method set mloc = 1 where methodId = 51";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 1 where methodId = 52";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 1 where methodId = 53";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 1 where methodId = 54";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 1 where methodId = 55";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 7 where methodId = 56";
				myStmt1.executeUpdate(sql);
				sql = "update method set mloc = 0 where methodId = 57";
				myStmt1.executeUpdate(sql);
				
				sql = "insert into detectedreference (referenceId, strategyId) value (7, 1)";
				myStmt.executeUpdate(sql);
				
				sql = "insert into detectedreference (referenceId, strategyId) value (7, 2)";
				myStmt.executeUpdate(sql);
				
				sql = "insert into detectedreference (referenceId, strategyId) value (6, 2)";
				myStmt.executeUpdate(sql);
				
				sql = "insert into detectedreference (referenceId, strategyId) value (17, 1)";
				myStmt.executeUpdate(sql);
				
				sql = "insert into detectedreference (referenceId, strategyId) value (17, 2)";
				myStmt.executeUpdate(sql);
			}
			
			PythonController runBat = new PythonController();
//		}catch (Exception e){
//			System.out.println("Something went wrong with your file.");
//		}	
	}
	public void emptyTable() throws SQLException{
		sql = "truncate table couplingrelationship";
		myStmt.executeUpdate(sql);
		
		sql = "truncate table field";
		myStmt.executeUpdate(sql);
		
		sql = "truncate table inheritancerelationship";
		myStmt.executeUpdate(sql);
		
		sql = "truncate table detectedmethod";
		myStmt.executeUpdate(sql);
		
		sql = "truncate table detectedreference";
		myStmt.executeUpdate(sql);
		
		sql = "SET FOREIGN_KEY_CHECKS=0";
		myStmt.executeUpdate(sql);
		sql = "truncate table method";
		myStmt.executeUpdate(sql);
		
		sql = "SET FOREIGN_KEY_CHECKS=0";
		myStmt.executeUpdate(sql);
		sql = "truncate table reference";
		myStmt.executeUpdate(sql);
		
		sql = "truncate table packageinpackage";
		myStmt.executeUpdate(sql);
		
		sql = "truncate table package";
		myStmt.executeUpdate(sql);
		
		sql = "truncate table project";
		myStmt.executeUpdate(sql);
	}
}