**free
ctl-opt dftname(SBGMSNRG) 
        option(*SRCSTMT)
        main(Main);

dcl-pr Shell extpgm('QCMDEXC');
    cmdstr  char(4096) const;
    cmdlen  packed(15:5) const;
end-pr;

dcl-ds gmail_params DTAARA(*AUTO : *USRCTL : 'QGPL/GMAILPARAM') qualified;
    Basedir     char(100);
    From        char(100);
    Pass        char(100);
end-ds;

dcl-c py_script 'sbgmsnr1.py';
dcl-s py_script_full_path char(255);
dcl-s params_string char(2048);
dcl-s command char(4096);

dcl-proc Main;
    dcl-pi *N extpgm; 
         To         char(50) const;
         Subject    char(50) const;
         Body       char(255) const;
         Attach     char(255) const;
    end-pi;
    
    in *lock gmail_params; 
    unlock gmail_params;

    py_script_full_path = %Trim(gmail_params.BaseDir)  +
                          '/bin/'                      +
     %Trim(py_script)             ;

    params_string= '"'+%Trim(To                   )+'" '+   
                   '"'+%Trim(gmail_params.From    )+'" '+   
                   '"'+%Trim(gmail_params.Pass    )+'" '+   
                   '"'+%Trim(Subject              )+'" '+   
                   '"'+%Trim(Body                 )+'" '+   
                   '"'+%Trim(Attach               )+'" '+
                           
    command = 'STRQSH CMD('''+
                            'python3 '                  +
                            %trim(py_script_full_path)  +
                            ' '                         +
                            params_string               +
                            ''')'                       ;
    monitor;
        Shell(command:4096);
    on-error;
    endmon;
end-proc;
