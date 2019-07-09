package controller;

import java.io.IOException;

public class PythonController {
	public PythonController() throws IOException{
		runPython();
	}
	public void runPython() throws IOException{
		String path="cmd /c start C:\\xampp\\htdocs\\codevis-MushroomFarm\\test.bat";
		Runtime rn=Runtime.getRuntime();
		Process pr=rn.exec(path);
	}
}
