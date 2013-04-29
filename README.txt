gp_finder_assistant_scripts
===========================

Best case workflow:
	1) Manually screen CSV-5 results from GP Finder 3
	2) use glycanLibraryMaker to make a searchable library for masshunter
	3) open the original datafile in masshunter 
		a) do either "Find compounds by chromatogram" or "Find by auto ms/ms"
		b) use "identify compounds by database" and select options to search by mass and RT
		c) select the library from step 2 and run the compound identifier.
		d) highlight results, rightclick and slect export. Export as a CSV
	4) Use results_intensity_comparison.py
		a) if compounds were found by "Find compounds by chromatogram" change intensityKey to "volume"
		b) if compounds were found by "Find by auto ms/ms" change intensityKey to "height"
		c) enter files to be compared and run the script
	5) use arrange-figures on output from step 4

----------  arrange-figures.py ------------
Use:
	This script will take a CSV-5 style GPFinder 3 output with abundances as integers or floats
	and it will output a set of annotated site-specific glycosylation figures. Output is in same
	directory as the script and is named as '[site number].jpg'. Possible issues that could break
	this script include two protein results with the same glycosylation site number and mis-formatted
	input.
	
prerequisites:
	* User must have installed python imaging library. See www.pythonware.com/products/pil/
	* User must have a folder with glycan images and required abundance images:
		- Abundance images must be those provided
		- Glycan images can be produced in glyco-workbench. USe 67% scale, compact form,
			and export to '.png' file
	
config options:
	sv3FileName : name of gp3 output file with abundances (entered as double quoted string)
	imageResourcesFolderName = name of folder containing glycan and abundance images (quoted string) 
	
	reduceCompositionListToSingleSpecies : repeats of a glycan composition will be summed and displayed
		as a single structure (True or False)
	drawOglycans : fixes spacing issues when drawing O-linked glycans (True or False)
	sortSiteAbundanceByIntensity : sort glycans by abundance left to right, top to bottom. (True or False)

----------  glycanLibraryMaker.py ------------
Use:
	This script will take a CSV-5 and output a csv that can be used
	in masshunter qual for compound searching
	
	
	