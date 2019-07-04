package ASTSeq_Generation;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;

import net.sf.json.JSONObject;

public class Analysis {

	@SuppressWarnings("deprecation")
	public static void main(String[] args) throws FileNotFoundException {
		
		FileInputStream fi = null;
		InputStreamReader is = null;
		BufferedReader br = null;
		//�����﷨�������ļ�
		File file1 = new File("D:\\java_project\\test\\src\\data\\Code.txt");
		//ע���ļ�
		File file2 = new File("D:\\java_project\\test\\src\\data\\Comment.txt");
		//����+ע���ļ�
		File file3 = new File("D:\\java_project\\test\\src\\data\\Combin.txt");
		//ɸѡ��ԭʼ����
		File file4 = new File("D:\\java_project\\test\\src\\data\\Result.txt");
		@SuppressWarnings("resource")
		PrintStream ps1 = new PrintStream(new FileOutputStream(file1));
		@SuppressWarnings("resource")
		PrintStream ps2 = new PrintStream(new FileOutputStream(file2));
		@SuppressWarnings("resource")
		PrintStream ps3 = new PrintStream(new FileOutputStream(file3));		
		@SuppressWarnings("resource")
		PrintStream ps4 = new PrintStream(new FileOutputStream(file4));
		
		try {
			String str = "";
			
			fi = new FileInputStream("D:\\java_project\\test\\src\\data\\train.txt");
			is = new InputStreamReader(fi);
			br = new BufferedReader(is);
			
			//�������г�ȡ5������
			int number = 50000;
			
			while((str = br.readLine())!=null&&number>0) {
				//��Json��������ȡ�����ע��
				JSONObject jsonObject = JSONObject.fromObject(str);
				String Ast = Parse.Prepare(jsonObject.getString("code"));
				String Comment = jsonObject.getString("nl");
				
				String Ast_2 = "";
				String Nl = "";
				char c[] = Ast.toCharArray();
				char d[] = Comment.toCharArray();
								
				for(int i=0;i<c.length;i++) {
					if(c[i]!='\n') {
						Ast_2 += c[i];
					}			
				}
				
				for(int i=0;i<d.length;i++) {
					if(d[i]!='.') {
						Nl += d[i];
					}else {
						Nl += d[i];
						break;
					}
				}
				//ɸѡ400���³��ȵ�����
                int num=0;
                for(int i=0;i<c.length;i++)
                {
                	if(Character.isSpace(c[i])) {
                		num++;
                	}
                }
                if(num<=400) {
                	ps1.println(Ast_2);
        			ps2.println(Nl);
        			ps3.println(Ast_2+" "+Nl);
        			ps4.println(str);
        			number--;
        			System.out.println(num);
                }			  				

			}

		}catch(FileNotFoundException e) {
			System.out.println("�Ҳ����ļ�");
		}catch(IOException e) {
			System.out.println("��ȡ�ļ�ʧ��");
		}finally {
			try {
				br.close();
				is.close();
				fi.close();
			}catch(IOException e) {
				e.printStackTrace();
			}
		}
	}
}

