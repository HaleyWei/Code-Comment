package ASTSeq_Generation;
import java.util.ArrayList;
import java.util.List;

import org.eclipse.jdt.core.dom.ASTNode;
import org.eclipse.jdt.core.dom.ChildListPropertyDescriptor;
import org.eclipse.jdt.core.dom.ChildPropertyDescriptor;
import org.eclipse.jdt.core.dom.StructuralPropertyDescriptor;


public class Traverse {

	public String str = ""; 
	@SuppressWarnings({ "unchecked", "rawtypes" })
	public void getAST(ASTNode node) {
		
		List listProperty = node.structuralPropertiesForType();
		boolean hasChildren = false;
		//当前节点子节点的列表
		List<ASTNode> childrenNodes = new ArrayList<>();
		
		//根据子节点类别，遍历抽象语法树，保存当前节点的子节点
		for(int i = 0; i<listProperty.size();i++) {
			StructuralPropertyDescriptor propertyDescriptor = (StructuralPropertyDescriptor) listProperty.get(i);
			
			if(propertyDescriptor instanceof ChildListPropertyDescriptor) {
				ChildListPropertyDescriptor childListPropertyDescriptor = (ChildListPropertyDescriptor)propertyDescriptor;
				Object children = node.getStructuralProperty(childListPropertyDescriptor);
			
				List<ASTNode> childrenNode = (List<ASTNode>)children;
				for(ASTNode child:childrenNode) {
					if(child==null) {
						continue;
					}
					childrenNodes.add(child);
				}
				hasChildren=true;
			}else if(propertyDescriptor instanceof ChildPropertyDescriptor) {
				ChildPropertyDescriptor childPropertyDescriptor = (ChildPropertyDescriptor)propertyDescriptor;
				Object child = node.getStructuralProperty(childPropertyDescriptor);
				ASTNode childNode = (ASTNode)child;
				
				if(childNode == null) {
					continue;
				}
				childrenNodes.add(childNode);
				hasChildren=true;
			}
		}
		//判断终端节点，结构化序列
		if(hasChildren) {
			
			str+="("+" "+node.getClass().getSimpleName()+" ";
			
			for(ASTNode Node:childrenNodes) {
				getAST(Node);
			}
			str+=")"+" "+node.getClass().getSimpleName()+" ";
		}else {
			str+="("+" "+node.getClass().getSimpleName()+"_"+node.toString()+" "+")"+" "+node.getClass().getSimpleName()+"_"+node.toString()+" ";
			
		}
	}
}
