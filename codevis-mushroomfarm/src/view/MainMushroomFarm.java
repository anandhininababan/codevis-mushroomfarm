package view;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.EventQueue;
import java.awt.Font;
import java.awt.Image;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.IOException;
import java.sql.SQLException;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.filechooser.FileNameExtensionFilter;

import controller.PythonController;

import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

import model.Project;
public class MainMushroomFarm {

	private JFrame frame;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					MainMushroomFarm window = new MainMushroomFarm();
					Dimension dim = Toolkit.getDefaultToolkit().getScreenSize();
					window.frame.setLocation(dim.width/2-window.frame.getSize().width/2, dim.height/2-window.frame.getSize().height/2);
					window.frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the application.
	 */
	public MainMushroomFarm() {
		initialize();
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		frame = new JFrame();
		frame.getContentPane().setBackground(new Color(192, 192, 192));
		frame.setBounds(100, 100, 1021, 703);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().setLayout(null);
		
		JButton btnVisualize = new JButton("Visualize");
		btnVisualize.setForeground(new Color(255, 255, 255));
		btnVisualize.setFont(new Font("Kristen ITC", Font.PLAIN, 20));
		btnVisualize.setBackground(new Color(128, 128, 128));
		btnVisualize.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				JFileChooser chooser = new JFileChooser();
				chooser.setDialogTitle("Open a Zip Java Project");
				chooser.addChoosableFileFilter(new FileNameExtensionFilter("ZIP Documents", "zip"));
				chooser.showOpenDialog(null);
				try{
					File f = chooser.getSelectedFile();
					String projectPath = f.getAbsolutePath();
					Project proj = new Project(projectPath);
					try {
						proj.parseHierarchy();
//						PythonController runBat = new PythonController();
					} catch (SQLException e2) {
						// TODO Auto-generated catch block
						e2.printStackTrace();
					}
				}catch(IOException e){
					System.out.println("No file was chosen.");
				}
			}
		});
		btnVisualize.setBounds(339, 329, 313, 45);
		frame.getContentPane().add(btnVisualize);
		
		JButton btnExit = new JButton("Exit");
		btnExit.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				System.exit(0);
			}
		});
		btnExit.setForeground(new Color(255, 255, 255));
		btnExit.setFont(new Font("Kristen ITC", Font.PLAIN, 20));
		btnExit.setBackground(new Color(128, 128, 128));
		btnExit.setBounds(340, 537, 316, 45);
		frame.getContentPane().add(btnExit);
		
		JLabel mushroom1 = new JLabel("");
		mushroom1.setBounds(69, 173, 143, 141);
		String path1 = "C:/xampp/htdocs/codevis-MushroomFarm/img/NewHappyMushroom.png";
		frame.getContentPane().add(mushroom1);
		ImageIcon MyImage1 = new ImageIcon(path1);
		Image img1 = MyImage1.getImage();
		Image newImg1 = img1.getScaledInstance(mushroom1.getWidth(), mushroom1.getHeight(), Image.SCALE_SMOOTH);
		ImageIcon image1 = new ImageIcon(newImg1);
		mushroom1.setIcon(image1);
		
		JLabel mushroom2 = new JLabel();
		mushroom2.setBounds(805, 112, 161, 162);
		String path2 = "C:/xampp/htdocs/codevis-MushroomFarm/img/NewSadMushroom.png";
		frame.getContentPane().add(mushroom2);
		ImageIcon MyImage2 = new ImageIcon(path2);
		Image img2 = MyImage2.getImage();
		Image newImg2 = img2.getScaledInstance(mushroom2.getWidth(), mushroom2.getHeight(), Image.SCALE_SMOOTH);
		ImageIcon image2 = new ImageIcon(newImg2);
		mushroom2.setIcon(image2);
		
		JLabel pictLabel = new JLabel();
		pictLabel.setBounds(158, 53, 688, 230);
		String path = "D:/S2/Tesis/capture pentng/title-mushroomfarm.png";
		frame.getContentPane().add(pictLabel);
		ImageIcon MyImage = new ImageIcon(path);
		Image img = MyImage.getImage();
		Image newImg = img.getScaledInstance(pictLabel.getWidth(), pictLabel.getHeight(), Image.SCALE_SMOOTH);
		ImageIcon image = new ImageIcon(newImg);
		//Image img = new ImageIcon(this.getClass().getResource("/MushGarden.png")).getImage();
		pictLabel.setIcon(image);
		String pathSettings = "C:/xampp/htdocs/codevis-MushroomFarm/img/settings.png";
		ImageIcon MyImage3 = new ImageIcon(pathSettings);
		Image img3 = MyImage3.getImage();
		String pathGuide = "C:/xampp/htdocs/codevis-MushroomFarm/img/open-book.png";
		ImageIcon MyImage4 = new ImageIcon(pathGuide);
		Image img4 = MyImage4.getImage();
		String pathAbout = "C:/xampp/htdocs/codevis-MushroomFarm/img/about.png";
		ImageIcon MyImage5 = new ImageIcon(pathAbout);
		Image img5 = MyImage5.getImage();
		
		JButton btnManageDetectionStrategies = new JButton("Manage detection strategies");
		btnManageDetectionStrategies.setForeground(Color.WHITE);
		btnManageDetectionStrategies.setFont(new Font("Kristen ITC", Font.PLAIN, 20));
		btnManageDetectionStrategies.setBackground(Color.GRAY);
		btnManageDetectionStrategies.setBounds(339, 398, 314, 45);
		frame.getContentPane().add(btnManageDetectionStrategies);
		
		JButton btnHelp = new JButton("Help");
		btnHelp.setForeground(Color.WHITE);
		btnHelp.setFont(new Font("Kristen ITC", Font.PLAIN, 20));
		btnHelp.setBackground(Color.GRAY);
		btnHelp.setBounds(340, 471, 314, 45);
		frame.getContentPane().add(btnHelp);
	}

}
