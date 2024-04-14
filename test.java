import java.util.ArrayList;

public class test{

    static String[] array = {"A", "B", "C", "D", "E"};
    static ArrayList<String> list = new ArrayList<String>();
    static int length = 6;

    public static void main(String[] args){
        constructor(6, "");
        System.out.println(list);
    }

    public static void constructor(int n, String s){
        if(n==0){
            list.add(s);
        } else {  
            for(String letter : array){
                String temp = s + letter;
                constructor(n-1, temp);
            } 
        }
    }
}