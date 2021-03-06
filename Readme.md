# Loads From Femap 

This program is responsible for extracting loads from finite elements generated in Femap in order to facilitate engineering calculations, mainly to extract critical load cases where many load cases are needed. For that some functions were created in this python program.

For all the examples shown in this manual cames from the analysis from this stiffined panel described below:


<img src = "https://github.com/lfml83/Femap_Extract_Loads/blob/main/panel.png?raw=true">


The Panel contains stiffeners along it splitting the panel in another four panels.

            
#### def <code style="color:red">elres(<code style="color:blue">[ids]</code>):</code>
This function is responsible for extracting the loads from the generated model including all load cases

##### list [ids] :
This list contains the elements ids that the operator want, and the kind of load that you want to extract.

<code style="color:red"> example 1:</code>

Panel1Nx=[5,4,,10,9,'Nx'] - all the results for membrane force in x direction<br>
Panel1Ny=[5,4,,10,9,'Ny'] - all the results for membrane force in y direction<br>
Panel1Nxy=[5,4,,10,9,'Ny'] - all the results for membrane force in xy direction<br>

**_program input :_** 

<img src="https://github.com/lfml83/Femap_Extract_Loads/blob/main/input.png?raw=true">



The kind of loads implementeds so far:<br>

**_Plate elements :_**

 * Nx - Menbrane force in X direction <br>
 * Ny - Menbrane force in X direction
 * Nxy - Menbrane force in XY direction
 * VM - maximum between bot and top Von Misses
 
**_Bar elements :_**

* Fx - Axial force<br>
* Sx - Axial Stress<br>
* MaxCS - Maximum combined Stress<br>
* MinCS - Minimum combined Stress<br>
* MaxBS - Maximum Bend Stress<br>
* MinBS - Maximum Bend Stress<br>

<code style="color:red"> example 2:</code>

- Another advantage to use elres function is to perform operations and take the results from this operations. To illustrate an example below, a joint calculation is shown.


<img src = "https://github.com/lfml83/Femap_Extract_Loads/blob/main/joint.png?raw=true">


**_program input :_** 


<img src = "https://github.com/lfml83/Femap_Extract_Loads/blob/main/Joint_input_result.png?raw=true">


**_program input :_** 

<img src = "https://github.com/lfml83/Femap_Extract_Loads/blob/main/Joint_output_result.png?raw=true">

