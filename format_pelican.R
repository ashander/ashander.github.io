if (FALSE) {
	# from node via r-script: working_dir = input[[1]]
}
if (TRUE) {
	# command line
	args = commandArgs()
	stopifnot(length(args) == 7)
	working_dir = args[6]
	infile = args[7]
}

require(rmarkdown, quiet = TRUE);

pelican_post <- function() {
	# format a pelican post with local figures
	ch_opts <- list(dev = 'svg', pelican = TRUE)
	k_hooks <- list(plot = function(x, options) {
				if (!is.null(options$pelican) && options$pelican)
					x <- paste0("\\{attach\\}", x)
				knitr::hook_plot_md(x, options)
})
	k_opts <- knitr_options(opts_chunk = ch_opts, knit_hooks = k_hooks)
	output_format(knitr = k_opts, pandoc = NULL,
		      base_format = rmarkdown::md_document(preserve_yaml = TRUE))
}

render_r_post <- function(input_name, output_name) {
	rmarkdown::render(input_name, output_format = pelican_post(),
                            output_file=output_name, quiet = TRUE,
                            encoding='UTF-8')
}


render_one <- function(rmd_file, wd=getwd(), rmd_pattern='*\\.rmd|\\.Rmd', md_pattern='.md'){
	owd <- getwd()
	setwd(wd)
	output_file <- gsub(rmd_pattern, md_pattern, rmd_file)
	render_r_post(input_name=rmd_file, output_name=output_file)
	setwd(owd)
	return(rmd_file)
}

render_one(rmd_file = infile, wd=working_dir)

# render_all(working_dir)
