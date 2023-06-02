#!/usr/bin/env zsh
#
# emulsion-zsh-completion
# =======================
#
# Zsh completion support for Emulsion (Epidemiological Multi-Level
# Simulation framwork)
#
# The contained completion routines provide support for completing:
#
#   * emulsion commands
#   * emulsion options
#   * emulsion folder filtering
#
#
# Installation
# ------------
#
# Emulsion completion should be automatically installed when
# installing Emulsion package through `pip`. Otherwise: copy it
# somewhere (e.g. ~/.emulsion-zsh-completion.sh) and put the
# following line in your .zshrc:
#
#     source ~/.emulsion-zsh-completion.sh
#
# Last modified 2023-05-31

_emulsion() {
    local cur opts cmds firstopt formats has_p command i MODEL PREVMODEL EMULSION_MODEL_PARAMS files

    if [[ ${words[1]} == "python" ]]
    then
      offset=2
    else
      offset=0
    fi

    cur="${words[CURRENT]}"
    prev="${words[CURRENT-1]}"

    cmds=("run" "diagrams" "show" "describe" "plot" "generate")
    opts=("-r" "-t" "--runs" "--time" "--aggregate" "--detail" "--level" "--seed" "--save" "--load" "--start-id" "--show-seed" "--table-params" "--no-count" "-p" "--param" "--log-params" "--view-model" "--output-dir" "--input-dir" "--figure-dir" "--code-path" "--format" "--silent" "--echo" "--deterministic" "--test" "--init")
    firstopt=("-V" "--version" "-L" "--license" "-h" "--help")
    formats=("png" "pdf" "jpg" "svg")
    plot=("--plot")
    has_p=0

    ## first argument: command or help or version
    if [[ ${CURRENT} -eq $(( 2 + offset )) ]]
    then
    	compadd -a cmds firstopt
    	return 0
    fi

    ## second argument: discard if version/help
    if [[ ${CURRENT} -eq $(( 3 + offset )) ]]
    then
    	case "$prev" in
    	    -V|--version|-h|--help|-L|--license)
    		return 0
    		;;
    	esac
    fi

    # identify command
    command=${words[$((2 + offset ))]}

    ## check if -p|--param already used
    for (( i=1; i < ${#words[@]}; i++ )); do
    	if [[ ${words[i]} = "-p" ]] || [[ ${words[i]} = "--param" ]]
    	then
    	    has_p=1
    	fi
    done

    # some commands accept fewer options
    case "$command" in
    	# nothing to propose after generate MODEL or describe MODEL
    	generate|describe)
    	    opts=()
    	    ;;
    	# only dirs and format after diagrams MODEL
	    diagrams)
	        opts=("--output-dir" "--figure-dir" "--format")
	        ;;
	    # only --modifiable and -p after show MODEL
	    show)
	        opts=("--modifiable" "-p" "--param")
	       ;;
    	# if already started -p|--param, only -p|--param available
    	*)
    	    if [ "$has_p" -eq 1 ]
    	    then
          		opts=("-p" "--param")
    	    fi
    	    ;;
    esac

    ## handle MODEL and OPTIONS
    case "$prev" in
    	## if previous argument is a model file, propose options
    	*.yaml)
    	    compadd -a opts
    	    return 0
    	    ;;
    	## some options require an additional parameter (no completion)
    	-r|--runs|-t|--time|--level|--seed|--start-id)
    	    return 0
    	    ;;
    	## option --format proposes several image formats
    	--format)
    	    compadd -a formats
    	    return 0
    	    ;;
    	## if -p|--param propose list of modifiable parameters
    	-p|--param)
    	    MODEL=${words[$(( 3 + offset ))]}
    	    if [ "$MODEL" = "--plot" ]
    	    then
    	    	MODEL=${COMP_WORDS[$(( 4 + offset ))]}
    	    fi
	        if [ -n "$MODEL" ]
	        then
    	    	if [ -z "$PREVMODEL" ] || [ "$MODEL" != "$PREVMODEL" ]
    		    then
    		      PREVMODEL=$MODEL
    		      EMULSION_MODEL_PARAMS=($(python -m emulsion show "$MODEL" --modifiable))
    		    fi
	        fi
    	    compadd -a EMULSION_MODEL_PARAMS
    	    return 0
    	    ;;
    	## some options require a folder
    	--output-dir|--input-dir|--figure-dir)
    	    _directories
    	    return 0
    	    ;;
    	## some options require a file
    	--load|--save)
    	    compadd -f *
    	    return 0
    	    ;;
    esac

    ## if at least 3 arguments (command [--plot] model) propose options
    if [ ${CURRENT} -gt $(( 4 + offset )) ]
    then
    	compadd -a opts
    	return 0
    fi

    if [ -n "$command" ]
    then
    	files=($(ls *.yaml 2>/dev/null))
    	if [ -z "$files" ]
    	then
    	    return 0
    	else
    	    if [ "$command" = "run" ] && [ "$prev" != "--plot" ]
    	    then
    	      compadd -a plot files
    		    return 0
    	    else
    	      compadd -a files
    		    return 0
    	    fi
    	fi
    else
    	return 0
    fi
return 0


}

compdef _emulsion emulsion
compdef _emulsion python -m emulsion

