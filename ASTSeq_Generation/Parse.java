package ASTSeq_Generation;

import org.eclipse.jdt.core.dom.AST;
import org.eclipse.jdt.core.dom.ASTParser;
import org.eclipse.jdt.core.dom.CompilationUnit;
import org.eclipse.jdt.core.dom.MethodDeclaration;


public class Parse {

	public static String Prepare(String s){
		String x = "class A{"+s
				 +"}";
        @SuppressWarnings("unused")
        //����
		String y ="class A{"
        		+ "public int test_1(char a) {\r\n" + 
        		"		return a;\r\n" + 
        		"	}"
        		+ "}";
        //����Ϊ�����﷨��
		ASTParser parser = ASTParser.newParser(AST.JLS11);
		parser.setSource(x.toCharArray());
		parser.setKind(ASTParser.K_COMPILATION_UNIT);
		//�����﷨������
		CompilationUnit cu = (CompilationUnit) parser.createAST(null);
		MethodNodeVisitor methodNodeVisitor = new MethodNodeVisitor();
		cu.accept(methodNodeVisitor);
		String B = null ;
		for(MethodDeclaration m : methodNodeVisitor.getMethodDecs()) {		

			Traverse A = new Traverse();	
			A.getAST(m);
	     	B = A.str;
		}
		//System.out.println(B);
		return B;
				
	}
					
}
