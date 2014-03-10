codes = {'Left':('3', '4', '100', '200', '400', '500'),
         'Right':('3', '4', '100', '200', '400', '500'),
         'LeftDual':('3', '4', '100', '200', '400', '500'),
         'RightDual':('3', '4', '100', '200', '400', '500'),
         'Audio':('1', '2', '64', '128')
         }


condLabels = {'Left':
                    [['3', 'dev_detected'],
                    ['4', 'dev_undetected'],
                    ['100', 'standard_corr'],
                    ['200', 'standard_incorr'],
                    ['400', 'standard_dev_seq_corr'],
                    ['500', 'standard_dev_seq_incorr']],
              'Right':
                    [['3', 'dev_detected'],
                    ['4', 'dev_undetected'],
                    ['100', 'standard_corr'],
                    ['200', 'standard_incorr'],
                    ['400', 'standard_dev_seq_corr'],
                    ['500', 'standard_dev_seq_incorr']],
              'LeftDual':
                    [['3', 'dev_detected'],
                    ['4', 'dev_undetected'],
                    ['100', 'standard_corr'],
                    ['200', 'standard_incorr'],
                    ['400', 'standard_dev_seq_corr'],
                    ['500', 'standard_dev_seq_incorr']],
              'RightDual':
                    [['3', 'dev_detected'],
                    ['4', 'dev_undetected'],
                    ['100', 'standard_corr'],
                    ['200', 'standard_incorr'],
                    ['400', 'standard_dev_seq_corr'],
                    ['500', 'standard_dev_seq_incorr']],
               'Audio':
                    [['1', 'std_tone'],
                     ['2', 'dev_tone'],
                     ['64', 'dev_detected'],
                     ['128', 'std_detected']]
                    }
                    
                    
runDict = {'Audio':['Run1', 'Run2']}


epMax = {'Left': '.4',
         'Right': '.4',
         'LeftDual': '.4',
         'RightDual': '.4',
         'Audio': '0.4'
        }
