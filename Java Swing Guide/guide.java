import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.*;

public class swingComponent {
    /* more resources of Swing Component
    https://www.tutorialspoint.com/swing/index.htm
    https://www.javatpoint.com/java-swing

    Advanced
    https://docs.oracle.com/javase/7/docs/api/javax/swing/package-summary.html */

    /* Pro tips from Chi Jian:
       if you stuck an error, or problem, or logical error, and you don't know how to solve it
       go GOOGLE, especially stackoverflow, it teaches me a lot when solving problems, if you have time,
       go research it by System.out.println(function) fill the function as the method, it will show the output,
       is important to know what output that method return */

    public static void main(String[] args) {
        // from here
        JFrame frame = new JFrame();
        frame.setTitle("title");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // click X will stop running
        frame.setSize(width, height);  // set size
        frame.setVisible(true);        // set the visibility to true or false
        frame.setLayout(layout); // BorderLayout, FlowLayout, GridLayout, GridBagLayout, etc or just null(means no layout)
        frame.getContentPane().setBackground(Color.white); // set background color for frame
        // to here is the necessary for JFrame

        JLabel label = new JLabel();

        // these function below can be used for most of the GUI component such as JLabel, JButton, etc

        label.setText("String"); // set text, JPanel, JFrame, JWindow cannot use this
        label.setFont(new Font("Calibri", Font.BOLD, size); // set the font style and size
        label.setBackground(Color.CYAN);  // set background color
        label.setForeground(Color.YELLOW);  // set the text part color

        label.setHorizontalAlignment(JLabel.CENTER; // set Horizontal alignment by LEFT CENTER RIGHT
        label.setVerticalAlignment(JLabel.CENTER); // set vertical alignment by TOP CENTER BOTTOM

        /* only work for image, don't use these two if you just use text only, button can use */
        label.setHorizontalTextPosition(JLabel.CENTER); // set Horizontal alignment by LEFT CENTER RIGHT
        label.setVerticalTextPosition(JLabel.CENTER);  // set vertical alignment by TOP CENTER BOTTOM

        label.setBorder(BorderFactory.createLineBorder(Color.BLACK, 1)); // set border thickness and color
        label.setBounds(coordX, coordY, width, height); // set location and size
        label.setSize(width, height); // set size
        label.setPreferredSize(new Dimension(width, height)); // set size (for layout only)
        label.setVisible(true); // set the visibility to true or false, some of GUI is on true

        // these function above can be used for most of the GUI component such as JLabel, JButton, etc

        JButton button = new JButton();

        button.addActionListener(e -> { // ActionListener is to give the button have some function such as click that button will do something
            // some code here
        });
        // or add it to class, example:
        class classes implements ActionListener { // note that ActionListener is class interface

            classes() {
                JButton button1 = new JButton();
                button1.addActionListener(this); // it will pass all the attributes in class
            }

            @Override
            public void actionPerformed(ActionEvent e) {
                if (e.getSource() == button) {
                    // some code here
                }
            }
        }

        // set Scrollbar
        JPanel panelForScroll = new JPanel();
        JScrollPane scroll = new JScrollPane(panelForScroll, JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED, JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
        scroll.setPreferredSize(new Dimension(1000, 1000)); // (width, height)
        // when you use scrollbar, that panelForScroll no need to set size, because it transfer to scroll, set the scroll size
        // and add it into JFrame or JPanel then done
        // How to add
        JFrame frameTest = new JFrame();
        frameTest.add(scroll);
        // or using JPanel, but remember need to add the panel into JFrame



        JPanel panel = new JPanel();
        // Layout - go google, hard to explain these part, but I will list out the method
        // IMPORTANT, when you want to set size while using layout, use setPreferredSize(new Dimension(width, height))
        // don't use setSize or setBounds, it will never work for layout unless is null

        /* h gap - horizontal gap
           v gap - vertical gap
           to create a gap between the GUI component
        */
        // BorderLayout
        panel.setLayout(null); // no layout
        panel.setLayout(new BorderLayout()); // BorderLayout(h gap, v gap))
        panel.add(button, BorderLayout.WEST);  // west, east, north ,south

        // FlowLayout
        panel.setLayout(new FlowLayout(FlowLayout.CENTER)); // FlowLayout(types, h gap, v gap)
        /* types
        CENTER - Stick to the center
        LEADING - Stick to the left
        TRAILING  - Stick to the right
        */

        // GridLayout
        panel.setLayout(new GridLayout(3, 3)); // GridLayout(row, column, h gap, v gap)
        // not recommend, because is fix row and column, if exceed then will add one column

        // GridBagLayout, to do this layout, need these to complete
        panel.setLayout(new GridBagLayout());
        GridBagConstraints bttConstraints = new GridBagConstraints();
        bttConstraints.gridx = 0;  // to set the where the x or row value
        bttConstraints.gridy = 0;  // to set the where the y or column value
        bttConstraints.insets = new Insets(10, 15, 10, 15);  // to set the gap
        // new Insets(top, left, bottom, right);
        panel.add(label, bttConstraints);  // add with the constraints

        // there are more layout, such as BoxLayout, GroupLayout, etc
        // but I only use three of them(BorderLayout, FlowLayout, GridBagLayout)
        // or just go no layout(need to plot x and y coordinate using setBounds)

        // Event for GUI components
        // ActionListener - something happen when someone touches the GUI, for Button, refer to button part
        // KeyListener - something happen whenever user type something
        // MouseListener - something happen whenever user click something
        // To use these need to: Got two method
        // Implement KeyListener
    }

    class methodkey1 {
        methodkey1() {
            JPanel panel = new JPanel();
            panel.addKeyListener(new KeyListener() {
                @Override
                public void keyTyped(KeyEvent e) {

                }

                @Override
                public void keyPressed(KeyEvent e) {

                }

                @Override
                public void keyReleased(KeyEvent e) {

                }
            });
        }
    }

    class methodkey2 implements KeyListener{
        methodkey2() {
            JPanel panel = new JPanel();
            panel.addKeyListener(this);
        }

        @Override
        public void keyTyped(KeyEvent e) {

        }

        @Override
        public void keyPressed(KeyEvent e) {

        }

        @Override
        public void keyReleased(KeyEvent e) {

        }
    }

    // Implement MouseListener
    class methodmouse1 {
        methodmouse1() {
            JPanel panel = new JPanel();
            panel.addMouseListener(new MouseListener() {
                @Override
                public void mouseClicked(MouseEvent e) {

                }

                @Override
                public void mousePressed(MouseEvent e) {

                }

                @Override
                public void mouseReleased(MouseEvent e) {

                }

                @Override
                public void mouseEntered(MouseEvent e) {

                }

                @Override
                public void mouseExited(MouseEvent e) {

                }
            });
        }
    }

    class methodmouse2 implements MouseListener {
        methodmouse2() {
            JPanel panel = new JPanel();
            panel.addMouseListener(this);
        }

        @Override
        public void mouseClicked(MouseEvent e) {

        }

        @Override
        public void mousePressed(MouseEvent e) {

        }

        @Override
        public void mouseReleased(MouseEvent e) {

        }

        @Override
        public void mouseEntered(MouseEvent e) {

        }

        @Override
        public void mouseExited(MouseEvent e) {

        }
    }
    // another one more is JTable, but I don't recommend to you, is hard
    // let me show you my code to these table, just create only, not including adding data into it and modify it

    class table {
        table() {
            JTable table = new JTable();
            table.setRowHeight(20);
            table.setFont(new Font("Default", Font.PLAIN, 16));

            JScrollPane scroll = new JScrollPane(table);
            scroll.setBounds(0, 0, 950, 650);
            DefaultTableModel tableModel = (DefaultTableModel) table.getModel(); // to enable to modify data feature()
            // adding column field
            tableModel.addColumn("Item Name");
            tableModel.addColumn("Price");
            tableModel.addColumn("Stocks");

            // to change the cell font when is editing
            JTextField textField = new JTextField();
            textField.setFont(new Font("Default", Font.PLAIN, 16));
            DefaultCellEditor dce = new DefaultCellEditor(textField);
            // to apply the text field to the column
            table.getColumnModel().getColumn(0).setCellEditor(dce);
            table.getColumnModel().getColumn(1).setCellEditor(dce);
            table.getColumnModel().getColumn(2).setCellEditor(dce);

            // not done yet, need to add, delete, change the data into table, and need to save

            // if you want to use, call me, I will help
        }
    }
}

// I think that's all, hopefully these will help you, if you still don't know how to do, can call me, I will help
