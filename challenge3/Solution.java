import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Scanner;

public class Solution {

  public static void search(String in, String out) throws IOException {
    FileWriter writer = new FileWriter(out);
    File file = new File(in);
    Scanner sc = new Scanner(file);

    List<String> docs = new ArrayList<String>();

    // Store all docs as strings
    int numDocs = Integer.parseInt(sc.nextLine());
    for (int doc_i = 0; doc_i < numDocs; doc_i++) {
      docs.add(sc.nextLine());
    }

    // Iterate through all queries
    int numQueries = Integer.parseInt(sc.nextLine());
    for (int query_i = 0; query_i < numQueries; query_i++) {
      String query = sc.nextLine();

      List<Integer> matches = new ArrayList<Integer>();
      boolean isFirstTerm = true;

      // Iterate through conjunctive terms to find docs common to all the terms
      List<String> conjunctives = Arrays.asList(query.split(" and "));
      for (String conjunctive : conjunctives) {
        List<Integer> conjunctiveMatches = new ArrayList<Integer>();

        // Try to parse the term to see if it is two disjunctive terms
        List<String> disjunctives = new ArrayList<String>();
        if (conjunctive.indexOf(" or ") != -1) {
          // Have two disjunctive terms
          disjunctives = Arrays.asList(
              conjunctive.substring(1, conjunctive.length()-1).split(" or "));
        } else {
          // Only one term
          disjunctives.add(conjunctive);
        }

        // Find docs that match with any of the disjunctive terms
        for (int doc_i = 0; doc_i < numDocs; doc_i++) {
          for (String term : disjunctives) {
            String[] terms = docs.get(doc_i).split(" ");
            for (int i = 1; i < terms.length; ++i)
                if (terms[i].equals(term)) {
                  conjunctiveMatches.add(doc_i);
                }
          }
        }

        if (isFirstTerm) {
          // If first term, add all matching docs
          matches.addAll(conjunctiveMatches);
          isFirstTerm = false;
        } else {
          // If not first term, retain all matching docs
          matches.retainAll(conjunctiveMatches);
        }
      }

      // Print out number of unique documents found
      HashSet<Integer> results = new HashSet<Integer>(matches);
      writer.write(String.valueOf(results.size()) + "\n");
    }

    writer.close();
  }

  public static void main(String[] args) throws IOException {
    if (args.length != 2) {
      System.out.println("Usage: java Solution in.txt out.txt");
      System.exit(0);
    }

    String in = args[0];
    String out = args[1];

    search(in, out);
  }
}
